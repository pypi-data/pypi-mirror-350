﻿"""
    Gather all full pipelines

"""
import nipype.interfaces.utility as niu
import nipype.pipeline.engine as pe


def rename_all_skull_petra_derivatives(params, main_workflow,
                                       skull_petra_pipe, datasink, pref_deriv,
                                       parse_str):

    # Rename in skull_petra_pipe
    if "skull_petra_pipe" in params.keys():

        # rename stereo_petra_skull_mask
        rename_stereo_petra = pe.Node(
            niu.Rename(), name="rename_stereo_petra")

        rename_stereo_petra.inputs.format_string =\
            pref_deriv + "_space-stereo_desc-petra_PDw"
        rename_stereo_petra.inputs.parse_string = parse_str
        rename_stereo_petra.inputs.keep_ext = True

        main_workflow.connect(
            skull_petra_pipe, 'outputnode.stereo_petra',
            rename_stereo_petra, 'in_file')

        main_workflow.connect(
            rename_stereo_petra, 'out_file',
            datasink, '@stereo_petra')

        if "headmask_petra_pipe" in params["skull_petra_pipe"]:

            # rename petra_head_stl
            rename_petra_head_stl = pe.Node(niu.Rename(),
                                            name="rename_petra_head_stl")
            rename_petra_head_stl.inputs.format_string = \
                pref_deriv + "_desc-petra_headmask"
            rename_petra_head_stl.inputs.parse_string = parse_str
            rename_petra_head_stl.inputs.keep_ext = True

            main_workflow.connect(
                skull_petra_pipe, 'outputnode.petra_head_stl',
                rename_petra_head_stl, 'in_file')

            main_workflow.connect(
                rename_petra_head_stl, 'out_file',
                datasink, '@petra_head_stl')

            # rename stereo_petra_head_mask
            rename_stereo_petra_head_mask = pe.Node(
                niu.Rename(), name="rename_stereo_petra_head_mask")

            rename_stereo_petra_head_mask.inputs.format_string =\
                pref_deriv + "_space-stereo_desc-petra_headmask"
            rename_stereo_petra_head_mask.inputs.parse_string = parse_str
            rename_stereo_petra_head_mask.inputs.keep_ext = True

            main_workflow.connect(
                skull_petra_pipe, 'outputnode.petra_head_mask',
                rename_stereo_petra_head_mask, 'in_file')

            main_workflow.connect(
                rename_stereo_petra_head_mask, 'out_file',
                datasink, '@stereo_petra_head_mask')

        if "skullmask_petra_pipe" in params["skull_petra_pipe"]:

            # rename petra_skull_stl
            rename_petra_skull_stl = pe.Node(
                niu.Rename(),
                name="rename_petra_skull_stl")

            rename_petra_skull_stl.inputs.format_string = \
                pref_deriv + "_desc-petra_skullmask"
            rename_petra_skull_stl.inputs.parse_string = parse_str
            rename_petra_skull_stl.inputs.keep_ext = True

            main_workflow.connect(
                skull_petra_pipe, 'outputnode.petra_skull_stl',
                rename_petra_skull_stl, 'in_file')

            main_workflow.connect(
                rename_petra_skull_stl, 'out_file',
                datasink, '@petra_skull_stl')

            # rename stereo_petra_skull_mask
            rename_stereo_petra_skull_mask = pe.Node(
                niu.Rename(), name="rename_stereo_petra_skull_mask")

            rename_stereo_petra_skull_mask.inputs.format_string =\
                pref_deriv + "_space-stereo_desc-petra_skullmask"
            rename_stereo_petra_skull_mask.inputs.parse_string = parse_str
            rename_stereo_petra_skull_mask.inputs.keep_ext = True

            main_workflow.connect(
                skull_petra_pipe, 'outputnode.petra_skull_mask',
                rename_stereo_petra_skull_mask, 'in_file')

            main_workflow.connect(
                rename_stereo_petra_skull_mask, 'out_file',
                datasink, '@stereo_petra_skull_mask')

            if "petra_skull_fov" in params["skull_petra_pipe"]:

                # rename robustpetra_skull_stl
                rename_robustpetra_skull_stl = pe.Node(
                    niu.Rename(), name="rename_robustpetra_skull_stl")

                rename_robustpetra_skull_stl.inputs.format_string = \
                    pref_deriv + "_desc-robustpetra_skullmask"
                rename_robustpetra_skull_stl.inputs.parse_string = parse_str
                rename_robustpetra_skull_stl.inputs.keep_ext = True

                main_workflow.connect(
                    skull_petra_pipe, 'outputnode.robustpetra_skull_stl',
                    rename_robustpetra_skull_stl, 'in_file')

                main_workflow.connect(
                    rename_robustpetra_skull_stl, 'out_file',
                    datasink, '@robustpetra_skull_stl')

                # rename stereo_robustpetra_skull_mask
                rename_stereo_robustpetra_skull_mask = pe.Node(
                    niu.Rename(), name="rename_stereo_robustpetra_skullmask")

                rename_stereo_robustpetra_skull_mask.inputs.format_string = \
                    pref_deriv + "_space-stereo_desc-robustpetra_skullmask"

                rename_stereo_robustpetra_skull_mask.inputs.parse_string = \
                    parse_str

                rename_stereo_robustpetra_skull_mask.inputs.keep_ext = True

                main_workflow.connect(
                    skull_petra_pipe, 'outputnode.robustpetra_skull_mask',
                    rename_stereo_robustpetra_skull_mask, 'in_file')

                main_workflow.connect(
                    rename_stereo_robustpetra_skull_mask, 'out_file',
                    datasink, '@stereo_robustpetra_skullmask')


def rename_all_skull_ct_derivatives(params, main_workflow,
                                    skull_ct_pipe, datasink, pref_deriv,
                                    parse_str):

    # Rename in skull_ct_pipe
    if "skull_ct_pipe" in params.keys():

        # rename ct_skull_mask
        rename_ct = pe.Node(niu.Rename(),
                            name="rename_ct")
        rename_ct.inputs.format_string = \
            pref_deriv + "_space-stereo_desc-ct_T2star"
        rename_ct.inputs.parse_string = parse_str
        rename_ct.inputs.keep_ext = True

        main_workflow.connect(
                skull_ct_pipe, "outputnode.stereo_ct",
                rename_ct, 'in_file')

        main_workflow.connect(
            rename_ct, 'out_file',
            datasink, '@stereo_ct')

        # rename ct_skull_mask
        rename_ct_skull_mask = pe.Node(niu.Rename(),
                                       name="rename_ct_skull_mask")
        rename_ct_skull_mask.inputs.format_string = \
            pref_deriv + "_space-stereo_desc-ct_skullmask"
        rename_ct_skull_mask.inputs.parse_string = parse_str
        rename_ct_skull_mask.inputs.keep_ext = True

        main_workflow.connect(
                skull_ct_pipe, "outputnode.stereo_ct_skull_mask",
                rename_ct_skull_mask, 'in_file')

        main_workflow.connect(
            rename_ct_skull_mask, 'out_file',
            datasink, '@ct_skull_mask')

        # rename ct_skull_stl
        rename_ct_skull_stl = pe.Node(niu.Rename(),
                                      name="rename_ct_skull_stl")
        rename_ct_skull_stl.inputs.format_string = \
            pref_deriv + "_desc-ct_skullmask"
        rename_ct_skull_stl.inputs.parse_string = parse_str
        rename_ct_skull_stl.inputs.keep_ext = True

        main_workflow.connect(
            skull_ct_pipe, 'outputnode.ct_skull_stl',
            rename_ct_skull_stl, 'in_file')

        main_workflow.connect(
            rename_ct_skull_stl, 'out_file',
            datasink, '@ct_skull_stl')

        if "ct_skull_fov" in params["skull_ct_pipe"]:

            # rename robustct_skull_stl
            rename_robustct_skull_stl = pe.Node(
                niu.Rename(), name="rename_robustct_skull_stl")

            rename_robustct_skull_stl.inputs.format_string = \
                pref_deriv + "_desc-robustct_skullmask"
            rename_robustct_skull_stl.inputs.parse_string = parse_str
            rename_robustct_skull_stl.inputs.keep_ext = True

            main_workflow.connect(
                skull_ct_pipe, 'outputnode.robustct_skull_stl',
                rename_robustct_skull_stl, 'in_file')

            main_workflow.connect(
                rename_robustct_skull_stl, 'out_file',
                datasink, '@robustct_skull_stl')

            # rename stereo_robustct_skull_mask
            rename_stereo_robustct_skull_mask = pe.Node(
                niu.Rename(), name="rename_stereo_robustct_skullmask")

            rename_stereo_robustct_skull_mask.inputs.format_string = \
                pref_deriv + "_space-stereo_desc-robustct_skullmask"

            rename_stereo_robustct_skull_mask.inputs.parse_string = \
                parse_str

            rename_stereo_robustct_skull_mask.inputs.keep_ext = True

            main_workflow.connect(
                skull_ct_pipe, 'outputnode.robustct_skull_mask',
                rename_stereo_robustct_skull_mask, 'in_file')

            main_workflow.connect(
                rename_stereo_robustct_skull_mask, 'out_file',
                datasink, '@stereo_robustct_skullmask')


def rename_all_skull_t1_derivatives(params, main_workflow,
                                    skull_t1_pipe, datasink, pref_deriv,
                                    parse_str):

    # Rename in skull_t1_pipe
    if "skull_t1_pipe" in params.keys():

        if "skullmask_t1_pipe" in params["skull_t1_pipe"]:

            # rename t1_skull_mask
            rename_t1_skull_mask = pe.Node(
                niu.Rename(), name="rename_t1_skull_mask")

            rename_t1_skull_mask.inputs.format_string = \
                pref_deriv + "_space-stereo_desc-t1_skullmask"
            rename_t1_skull_mask.inputs.parse_string = parse_str
            rename_t1_skull_mask.inputs.keep_ext = True

            main_workflow.connect(
                    skull_t1_pipe, "outputnode.t1_skull_mask",
                    rename_t1_skull_mask, 'in_file')

            main_workflow.connect(
                rename_t1_skull_mask, 'out_file',
                datasink, '@t1_skull_mask')

            # rename t1_skull_stl
            rename_t1_skull_stl = pe.Node(
                niu.Rename(),
                name="rename_t1_skull_stl")

            rename_t1_skull_stl.inputs.format_string = \
                pref_deriv + "_desc-t1_skullmask"
            rename_t1_skull_stl.inputs.parse_string = parse_str
            rename_t1_skull_stl.inputs.keep_ext = True

            main_workflow.connect(
                skull_t1_pipe, 'outputnode.t1_skull_stl',
                rename_t1_skull_stl, 'in_file')

            main_workflow.connect(
                rename_t1_skull_stl, 'out_file',
                datasink, '@t1_skull_stl')

            if "t1_skull_fov" in params["skull_t1_pipe"]:

                # rename robustt1_skull_stl
                rename_robustt1_skull_stl = pe.Node(
                    niu.Rename(), name="rename_robustt1_skull_stl")

                rename_robustt1_skull_stl.inputs.format_string = \
                    pref_deriv + "_desc-robustt1_skullmask"
                rename_robustt1_skull_stl.inputs.parse_string = parse_str
                rename_robustt1_skull_stl.inputs.keep_ext = True

                main_workflow.connect(
                    skull_t1_pipe, 'outputnode.robustt1_skull_stl',
                    rename_robustt1_skull_stl, 'in_file')

                main_workflow.connect(
                    rename_robustt1_skull_stl, 'out_file',
                    datasink, '@robustt1_skull_stl')

                # rename stereo_robustt1_skull_mask
                rename_stereo_robustt1_skull_mask = pe.Node(
                    niu.Rename(), name="rename_stereo_robustt1_skullmask")

                rename_stereo_robustt1_skull_mask.inputs.format_string = \
                    pref_deriv + "_space-stereo_desc-robustt1_skullmask"

                rename_stereo_robustt1_skull_mask.inputs.parse_string = \
                    parse_str

                rename_stereo_robustt1_skull_mask.inputs.keep_ext = True

                main_workflow.connect(
                    skull_t1_pipe, 'outputnode.robustt1_skull_mask',
                    rename_stereo_robustt1_skull_mask, 'in_file')

                main_workflow.connect(
                    rename_stereo_robustt1_skull_mask, 'out_file',
                    datasink, '@stereo_robustt1_skullmask')

        if "headmask_t1_pipe" in params["skull_t1_pipe"]:

            # rename t1_head_mask
            rename_t1_head_mask = pe.Node(
                niu.Rename(), name="rename_t1_head_mask")

            rename_t1_head_mask.inputs.format_string = \
                pref_deriv + "_space-stereo_desc-t1_headmask"
            rename_t1_head_mask.inputs.parse_string = parse_str
            rename_t1_head_mask.inputs.keep_ext = True

            main_workflow.connect(
                skull_t1_pipe, 'outputnode.t1_head_mask',
                rename_t1_head_mask, 'in_file')

            main_workflow.connect(
                rename_t1_head_mask, 'out_file',
                datasink, '@t1_head_mask')


# ############################# ANGIO
def rename_all_angio_derivatives(params, main_workflow, angio_pipe, datasink,
                                 pref_deriv, parse_str):
    # Rename in skull_t1_pipe
    if "angio_pipe" in params.keys() or "angio_quick_pipe" in params.keys():

        # rename_stereo_angio_mask
        rename_stereo_angio_mask = pe.Node(
            niu.Rename(),
            name="rename_stereo_angio_mask")
        rename_stereo_angio_mask.inputs.format_string = \
            pref_deriv + "_space-stereo_desc-angio_mask"
        rename_stereo_angio_mask.inputs.parse_string = parse_str
        rename_stereo_angio_mask.inputs.keep_ext = True

        main_workflow.connect(
            angio_pipe, 'outputnode.stereo_angio_mask',
            rename_stereo_angio_mask, 'in_file')

        main_workflow.connect(
            rename_stereo_angio_mask, 'out_file',
            datasink, '@stereo_angio_mask')

        # rename_stereo_angio
        rename_stereo_angio = pe.Node(
            niu.Rename(),
            name="rename_stereo_angio")
        rename_stereo_angio.inputs.format_string = \
            pref_deriv + "_space-stereo_angio"
        rename_stereo_angio.inputs.parse_string = parse_str
        rename_stereo_angio.inputs.keep_ext = True

        main_workflow.connect(
            angio_pipe, 'outputnode.stereo_angio',
            rename_stereo_angio, 'in_file')

        main_workflow.connect(
            rename_stereo_angio, 'out_file',
            datasink, '@stereo_angio')

        if "angio_pipe" in params.keys():

            # rename_stereo_brain_angio
            rename_stereo_brain_angio = pe.Node(
                niu.Rename(),
                name="rename_stereo_brain_angio")
            rename_stereo_brain_angio.inputs.format_string = \
                pref_deriv + "_space-stereo_desc-brain_angio"
            rename_stereo_brain_angio.inputs.parse_string = parse_str
            rename_stereo_brain_angio.inputs.keep_ext = True

            main_workflow.connect(
                angio_pipe, 'outputnode.stereo_brain_angio',
                rename_stereo_brain_angio, 'in_file')

            main_workflow.connect(
                rename_stereo_brain_angio, 'out_file',
                datasink, '@stereo_brain_angio')
