# Copyright (C) 2009-2017, Ecole Polytechnique Federale de Lausanne (EPFL) and
# Hospital Center and University of Lausanne (UNIL-CHUV), Switzerland
# All rights reserved.
#
#  This software is distributed under the open-source license Modified BSD.

""" The ANTs module provides functions for interfacing with ANTs registration toolbox missing in nipype or modified
"""
try:
    from traitsui.api import *
    from traits.api import *

except ImportError:
    from enthought.traits.api import *
    from enthought.traits.ui.api import *

import os
import glob

from nipype.interfaces.base import traits, isdefined, CommandLine, CommandLineInputSpec,\
    TraitedSpec, InputMultiPath, OutputMultiPath, BaseInterface, BaseInterfaceInputSpec

from nipype.interfaces.ants.resampling import ApplyTransforms

class MultipleANTsApplyTransformsInputSpec(BaseInterfaceInputSpec):
    input_images = InputMultiPath(File(desc='files to be registered', mandatory = True, exists = True))
    transforms = InputMultiPath(File(exists=True), mandatory=True,
                                desc='transform files: will be applied in reverse order. For '
                                'example, the last specified transform will be applied first.')
    reference_image = File(mandatory = True, exists = True)
    interpolation = traits.Enum('Linear',
                                'NearestNeighbor',
                                'CosineWindowedSinc',
                                'WelchWindowedSinc',
                                'HammingWindowedSinc',
                                'LanczosWindowedSinc',
                                'MultiLabel',
                                'Gaussian',
                                'BSpline',
                                usedefault=True)
    default_value = traits.Float(0)
    out_postfix = traits.Str("_transformed", usedefault=True)

class MultipleANTsApplyTransformsOutputSpec(TraitedSpec):
    output_images = OutputMultiPath(File())

class MultipleANTsApplyTransforms(BaseInterface):
    input_spec = MultipleANTsApplyTransformsInputSpec
    output_spec = MultipleANTsApplyTransformsOutputSpec

    def _run_interface(self, runtime):
        for input_image in self.inputs.input_images:
            ax = ApplyTransforms(input_image = input_image, reference_image=self.inputs.reference_image, interpolation=self.inputs.interpolation, transforms=self.inputs.transforms, out_postfix=self.inputs.out_postfix, default_value=self.inputs.default_value)
            ax.run()
        return runtime

    def _list_outputs(self):
        outputs = self._outputs().get()
        outputs['output_images'] = glob.glob(os.path.abspath("*.nii.gz"))
        return outputs