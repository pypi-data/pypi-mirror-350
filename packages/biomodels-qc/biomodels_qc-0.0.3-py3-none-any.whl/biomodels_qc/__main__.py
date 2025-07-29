""" Command-line program for quality controlling BioModels and converting entries to alternative formats

:Author: Jonathan Karr <karr@mssm.edu>
:Date: 2021-04-24
:Copyright: 2021, BioSimulations Team
:License: MIT
"""

from .convert import convert_entry, AltSbmlFormat
from .utils import build_combine_archive
from .validation import validate_entry
from .warnings import BiomodelsQcWarning
from biosimulators_utils.combine.io import CombineArchiveWriter
from biosimulators_utils.data_model import Person
from biosimulators_utils.utils.core import flatten_nested_list_of_strings
from biosimulators_utils.warnings import BioSimulatorsWarning
import biomodels_qc
import cement
import glob
import os
import termcolor
import warnings


class BaseController(cement.Controller):
    """ Base controller for command line application """

    class Meta:
        label = 'base'
        help = (
            "Program for quality controlling entries of the BioModels database and converting "
            "the primary files for entries to alternative formats."
        )
        description = (
            "Program for quality controlling the BioModels database."
        )
        arguments = [
            (['-v', '--version'], dict(
                action='version',
                version=biomodels_qc.__version__,
            )),
        ]

    @cement.ex(hide=True)
    def _default(self):
        self._parser.print_help()


class ValidateEntryController(cement.Controller):
    """ Controller for validating an entry of the BioModels database. """

    class Meta:
        label = 'validate'
        stacked_on = 'base'
        stacked_type = 'nested'
        help = "Validate an entry of the BioModels database."
        description = "Validate all of the files that comprise an entry of the BioModels database."
        arguments = [
            (
                ['dir'],
                dict(
                    type=str,
                    help='Path to a directory which contains the files for an entry of the BioModels database',
                ),
            ),
            (
                ['--ext'],
                dict(
                    type=str,
                    action='append',
                    default=None,
                    help='File extension to validate (.e.g, `.png`). Default: validate all files.',
                ),
            ),
            (
                ['--file'],
                dict(
                    type=str,
                    action='append',
                    default=None,
                    help='Path relative to `dir` of file to validate (.e.g, `model.xml`). Default: validate all files.',
                ),
            ),
            (
                ['--simulator'],
                dict(
                    type=str,
                    action='append',
                    default=None,
                    help=(
                        'Simulator to use to validate the executability of SED-ML files in the entry (.e.g, `copasi` or `copasi:4.30.240`)'
                    ),
                ),
            ),
            (
                ['--do-not-display-warnings'],
                dict(
                    action='store_true',
                    help='Do not display warnings.',
                ),
            ),
        ]

    @cement.ex(hide=True)
    def _default(self):
        args = self.app.pargs

        if args.simulator is None:
            simulators = None
        else:
            simulators = []
            for simulator in args.simulator:
                id, _, version = simulator.partition(':')
                simulators.append({'id': id, 'version': version or None})

        with warnings.catch_warnings():
            if args.do_not_display_warnings:
                warnings.simplefilter("ignore", BiomodelsQcWarning)
                warnings.simplefilter("ignore", BioSimulatorsWarning)
            entry_errors, entry_warnings = validate_entry(args.dir, file_extensions=args.ext, filenames=args.file, simulators=simulators)

        if entry_warnings:
            if args.do_not_display_warnings:
                entry_warnings = [[(
                    'The entry at `{}` may be invalid. Rerun this validation without `--do-not-display-warnings` '
                    'to display additional information.'
                ).format(args.dir)]]
            else:
                entry_warnings = [['The entry at `{}` may be invalid.'.format(args.dir), entry_warnings]]
            print(termcolor.colored(flatten_nested_list_of_strings(entry_warnings), 'yellow'))

        if entry_errors:
            entry_errors = [['The entry at `{}` is invalid.'.format(args.dir), entry_errors]]
            raise SystemExit(termcolor.colored(flatten_nested_list_of_strings(entry_errors), 'red'))

        if not entry_warnings:
            print('The entry at `{}` is valid.'.format(args.dir))


class BuildCombineArchiveController(cement.Controller):
    """ Controller for packaging a directory for an entry of BioModels into a COMBINE/OMEX archive. """

    class Meta:
        label = 'build-archive'
        stacked_on = 'base'
        stacked_type = 'nested'
        help = "Build a COMBINE/OMEX archive for an entry of BioModels."
        description = "Build a directory for an entry of BioModels into a COMBINE/OMEX archive."
        arguments = [
            (
                ['dir'],
                dict(
                    type=str,
                    help='Path to a directory to package into a COMBINE/OMEX archive',
                ),
            ),
            (
                ['archive'],
                dict(
                    type=str,
                    help='Path to save COMBINE/OMEX archive',
                ),
            ),
            (
                ['--master'],
                dict(
                    type=str,
                    action='append',
                    default=None,
                    help='Path to a file that should be marked as `master`. Default: mark all SED-ML files as master.',
                ),
            ),
            (
                ['--description'],
                dict(
                    type=str,
                    default=None,
                    help='Description of the archive.',
                ),
            ),
            (
                ['--author'],
                dict(
                    type=str,
                    action='append',
                    default=[],
                    help='Author of the archive (Family Name, Given Name).',
                ),
            ),
            (
                ['--do-not-display-warnings'],
                dict(
                    action='store_true',
                    help='Do not display warnings.',
                ),
            ),
        ]

    @cement.ex(hide=True)
    def _default(self):
        args = self.app.pargs

        if args.master:
            master_filenames = args.master
        else:
            master_filenames = glob.glob(os.path.join(args.dir, '**', '*.sedml'), recursive=True)
        master_rel_filenames = [os.path.relpath(master_filename, args.dir) for master_filename in master_filenames]

        description = args.description.strip() if args.description else None
        authors = []
        for author in args.author:
            family_name, _, given_name = author.partition(',')
            family_name = family_name.strip() or None
            given_name = given_name.strip() or None
            authors.append(Person(family_name=family_name, given_name=given_name))

        archive = build_combine_archive(args.dir, master_rel_filenames,
                                        description=description, authors=authors)

        with warnings.catch_warnings():
            if args.do_not_display_warnings:
                warnings.simplefilter("ignore", BiomodelsQcWarning)
                warnings.simplefilter("ignore", BioSimulatorsWarning)
            CombineArchiveWriter().run(archive, args.dir, args.archive)


class BuildOmexManifestController(cement.Controller):
    """ Controller for building an OMEX manifest file for a directory for an entry of BioModels. """

    class Meta:
        label = 'build-manifest'
        stacked_on = 'base'
        stacked_type = 'nested'
        help = "Build an OMEX manifest file archive for an entry of BioModels."
        description = "Build an OMEX manifest file file a directory for an entry of BioModels."
        arguments = [
            (
                ['dir'],
                dict(
                    type=str,
                    help='Path to a directory to build a manifest for',
                ),
            ),
            (
                ['manifest_filename'],
                dict(
                    metavar='manifest-filename',
                    type=str,
                    help='Path to save manifest',
                ),
            ),
            (
                ['--master'],
                dict(
                    type=str,
                    action='append',
                    default=None,
                    help='Path to a file that should be marked as `master`. Default: mark all SED-ML files as master.',
                ),
            ),
        ]

    @cement.ex(hide=True)
    def _default(self):
        args = self.app.pargs

        if args.master:
            master_filenames = args.master
        else:
            master_filenames = glob.glob(os.path.join(args.dir, '**', '*.sedml'), recursive=True)
        master_rel_filenames = [os.path.relpath(master_filename, args.dir) for master_filename in master_filenames]

        archive = build_combine_archive(args.dir, master_rel_filenames)

        CombineArchiveWriter().write_manifest(archive.contents, args.manifest_filename)


class ConvertEntryProjectController(cement.Controller):
    """ Controller for converting the primary files for an entry of the BioModels database to alternative formats. """

    class Meta:
        label = 'convert'
        stacked_on = 'base'
        stacked_type = 'nested'
        help = "Convert the primary files for an entry of the BioModels database to alternative formats."
        description = (
            "Convert the primary files for an entry of the BioModels database to alternative formats "
            "such as BioPAX, MATLAB/Octave, and XPP."
        )
        arguments = [
            (
                ['dir'],
                dict(
                    type=str,
                    help='Path to a directory which contains the files for an entry of the BioModels database',
                ),
            ),
            (
                ['--format'],
                dict(
                    type=str,
                    action='append',
                    default=None,
                    help=(
                        'Format to convert SBML files to ({}). Default: convert SBML files to all alternative formats.'.format(
                            ', '.join(AltSbmlFormat.__members__.keys())
                        )
                    ),
                ),
            ),
            (
                ['--do-not-display-warnings'],
                dict(
                    action='store_true',
                    help='Do not display warnings.',
                ),
            ),
        ]

    @cement.ex(hide=True)
    def _default(self):
        args = self.app.pargs
        if args.format:
            alt_sbml_formats = [AltSbmlFormat[format] for format in args.format]
        else:
            alt_sbml_formats = AltSbmlFormat.__members__.values()

        with warnings.catch_warnings():
            if args.do_not_display_warnings:
                warnings.simplefilter("ignore", BiomodelsQcWarning)
                warnings.simplefilter("ignore", BioSimulatorsWarning)
            convert_entry(args.dir, alt_sbml_formats=alt_sbml_formats)


class App(cement.App):
    """ Command line application """
    class Meta:
        label = 'biomodels-qc'
        base_controller = 'base'
        handlers = [
            BaseController,
            ValidateEntryController,
            BuildCombineArchiveController,
            BuildOmexManifestController,
            ConvertEntryProjectController,
        ]


def main():
    with App() as app:
        app.run()
