#!/usr/bin/env python

# ...

import shutil,os
root = __file__[:__file__.rfind('/')]
lib = os.environ['HOME']+'/lib'

sos = ["libOpenCL.so", "libSvtAv1Enc.so", "libabsl_bad_any_cast_impl.so", "libabsl_bad_optional_access.so", "libabsl_bad_variant_access.so", "libabsl_base.so", "libabsl_city.so", "libabsl_civil_time.so", "libabsl_cord.so", "libabsl_cord_internal.so", "libabsl_cordz_functions.so", "libabsl_cordz_handle.so", "libabsl_cordz_info.so", "libabsl_cordz_sample_token.so", "libabsl_crc32c.so", "libabsl_crc_cord_state.so", "libabsl_crc_cpu_detect.so", "libabsl_crc_internal.so", "libabsl_debugging_internal.so", "libabsl_demangle_internal.so", "libabsl_die_if_null.so", "libabsl_examine_stack.so", "libabsl_exponential_biased.so", "libabsl_failure_signal_handler.so", "libabsl_flags_commandlineflag.so", "libabsl_flags_commandlineflag_internal.so", "libabsl_flags_config.so", "libabsl_flags_internal.so", "libabsl_flags_marshalling.so", "libabsl_flags_parse.so", "libabsl_flags_private_handle_accessor.so", "libabsl_flags_program_name.so", "libabsl_flags_reflection.so", "libabsl_flags_usage.so", "libabsl_flags_usage_internal.so", "libabsl_graphcycles_internal.so", "libabsl_hash.so", "libabsl_hashtablez_sampler.so", "libabsl_int128.so", "libabsl_kernel_timeout_internal.so", "libabsl_leak_check.so", "libabsl_log_entry.so", "libabsl_log_flags.so", "libabsl_log_globals.so", "libabsl_log_initialize.so", "libabsl_log_internal_check_op.so", "libabsl_log_internal_conditions.so", "libabsl_log_internal_format.so", "libabsl_log_internal_globals.so", "libabsl_log_internal_log_sink_set.so", "libabsl_log_internal_message.so", "libabsl_log_internal_nullguard.so", "libabsl_log_internal_proto.so", "libabsl_log_severity.so", "libabsl_log_sink.so", "libabsl_low_level_hash.so", "libabsl_malloc_internal.so", "libabsl_periodic_sampler.so", "libabsl_random_distributions.so", "libabsl_random_internal_distribution_test_util.so", "libabsl_random_internal_platform.so", "libabsl_random_internal_pool_urbg.so", "libabsl_random_internal_randen.so", "libabsl_random_internal_randen_hwaes.so", "libabsl_random_internal_randen_hwaes_impl.so", "libabsl_random_internal_randen_slow.so", "libabsl_random_internal_seed_material.so", "libabsl_random_seed_gen_exception.so", "libabsl_random_seed_sequences.so", "libabsl_raw_hash_set.so", "libabsl_raw_logging_internal.so", "libabsl_scoped_set_env.so", "libabsl_spinlock_wait.so", "libabsl_stacktrace.so", "libabsl_status.so", "libabsl_statusor.so", "libabsl_str_format_internal.so", "libabsl_strerror.so", "libabsl_string_view.so", "libabsl_strings.so", "libabsl_strings_internal.so", "libabsl_symbolize.so", "libabsl_synchronization.so", "libabsl_throw_delegate.so", "libabsl_time.so", "libabsl_time_zone.so", "libaom.so", "libavcodec.so", "libavformat.so", "libavutil.so", "libbluray.so", "libbrotlicommon.so", "libbrotlidec.so", "libbrotlienc.so", "libdav1d.so", "libfontconfig.so", "libfreetype.so", "libfribidi.so", "libgme.so", "libgraphite2.so", "libharfbuzz-cairo.so", "libharfbuzz-gobject.so", "libharfbuzz-subset.so", "libharfbuzz.so", "libjpeg.so", "liblcms2.so", "libmp3lame.so", "libmpg123.so", "libogg.so", "libopencore-amrnb.so", "libopencore-amrwb.so", "libopencv_aruco.so", "libopencv_bgsegm.so", "libopencv_bioinspired.so", "libopencv_calib3d.so", "libopencv_ccalib.so", "libopencv_core.so", "libopencv_datasets.so", "libopencv_dnn.so", "libopencv_dnn_objdetect.so", "libopencv_dnn_superres.so", "libopencv_dpm.so", "libopencv_face.so", "libopencv_features2d.so", "libopencv_flann.so", "libopencv_freetype.so", "libopencv_fuzzy.so", "libopencv_gapi.so", "libopencv_hfs.so", "libopencv_highgui.so", "libopencv_img_hash.so", "libopencv_imgcodecs.so", "libopencv_imgproc.so", "libopencv_intensity_transform.so", "libopencv_line_descriptor.so", "libopencv_mcc.so", "libopencv_ml.so", "libopencv_objdetect.so", "libopencv_optflow.so", "libopencv_phase_unwrapping.so", "libopencv_photo.so", "libopencv_plot.so", "libopencv_quality.so", "libopencv_rapid.so", "libopencv_reg.so", "libopencv_rgbd.so", "libopencv_saliency.so", "libopencv_shape.so", "libopencv_signal.so", "libopencv_stereo.so", "libopencv_stitching.so", "libopencv_structured_light.so", "libopencv_superres.so", "libopencv_surface_matching.so", "libopencv_text.so", "libopencv_tracking.so", "libopencv_video.so", "libopencv_videoio.so", "libopencv_videostab.so", "libopencv_wechat_qrcode.so", "libopencv_xfeatures2d.so", "libopencv_ximgproc.so", "libopencv_xobjdetect.so", "libopencv_xphoto.so", "libopenjp2.so", "libopenmpt.so", "libopus.so", "libpng16.so", "librav1e.so", "libsharpyuv.so", "libsoxr-lsr.so", "libsoxr.so", "libsrt.so", "libssh.so", "libswresample.so", "libswscale.so", "libtheora.so", "libtheoradec.so", "libtheoraenc.so", "libtiff.so", "libtiffxx.so", "libudfread.so", "libvo-amrwbenc.so", "libvorbis.so", "libvorbisenc.so", "libvorbisfile.so", "libvpx.so", "libwebp.so", "libwebpmux.so", "libx264.so", "libx265.so", "libxvidcore.so"]

long_description="""
OpenCV is raising funds to keep the library free for everyone, and we need the support of the entire community to do it.
"""
current_directory = os.path.dirname(os.path.abspath(__file__))
readme_path = os.path.join(current_directory, 'README.md')
try:
    with open(readme_path, 'r', encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    pass

from distutils.core import setup
from setuptools import setup, Extension

setup(name='opencv-aipy',
      version='4.10.0',
      description='Wrapper package for OpenCV python bindings',
      author='OpenCV Development Team',
      author_email='support@qpython.org',
      url='https://pypi.org/project/opencv-python/',
      data_files=[(lib, sos)],
      packages=['cv2',],
      package_data={
        'cv2':[
"Error/*",
"__init__.py",
"__init__.pyi",
"aruco/*",
"barcode/*",
"bgsegm/*",
"bioinspired/*",
"ccm/*",
"colored_kinfu/*",
"config-3.12.py",
"config.py",
"cuda/*",
"datasets/*",
"detail/*",
"dnn/*",
"dnn_superres/*",
"dpm/*",
"dynafu/*",
"face/*",
"fisheye/*",
"flann/*",
"freetype/*",
"ft/*",
"gapi/*",
"gapi/core/*",
"gapi/core/cpu/*",
"gapi/core/fluid/*",
"gapi/core/ocl/*",
"gapi/ie/*",
"gapi/ie/detail/*",
"gapi/imgproc/*",
"gapi/imgproc/fluid/*",
"gapi/oak/*",
"gapi/onnx/*",
"gapi/onnx/ep/*",
"gapi/ot/*",
"gapi/ot/cpu/*",
"gapi/ov/*",
"gapi/own/*",
"gapi/own/detail/*",
"gapi/render/*",
"gapi/render/ocv/*",
"gapi/streaming/*",
"gapi/video/*",
"gapi/wip/*",
"gapi/wip/draw/*",
"gapi/wip/gst/*",
"gapi/wip/onevpl/*",
"hfs/*",
"img_hash/*",
"intensity_transform/*",
"ipp/*",
"kinfu/*",
"kinfu/detail/*",
"large_kinfu/*",
"legacy/*",
"line_descriptor/*",
"linemod/*",
"load_config_py2.py",
"load_config_py3.py",
"mat_wrapper/*",
"mcc/*",
"misc/*",
"ml/*",
"motempl/*",
"multicalib/*",
"ocl/*",
"ogl/*",
"omnidir/*",
"optflow/*",
"parallel/*",
"phase_unwrapping/*",
"plot/*",
"ppf_match_3d/*",
"py.typed",
"python-3.12/*",
"quality/*",
"rapid/*",
"reg/*",
"rgbd/*",
"saliency/*",
"samples/*",
"segmentation/*",
"signal/*",
"stereo/*",
"structured_light/*",
"text/*",
"typing/*",
"utils/*",
"utils/fs/*",
"utils/nested/*",
"videoio_registry/*",
"videostab/*",
"wechat_qrcode/*",
"xfeatures2d/*",
"ximgproc/*",
"ximgproc/segmentation/*",
"xphoto/*",

        ]
},
      long_description=long_description,
      long_description_content_type="text/markdown",
      classifiers=[
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: Information Technology",
            "Intended Audience :: End Users/Desktop",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: Android",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.12",
            "Topic :: Software Development",
        ],
      license="Apache Software License (Apache 2.0)",
      install_requires=["numpy-aipy"],
      python_requires='==3.12.*'
     )

for item in sos:
    try:
        shutil.copy(root+'/'+item, lib)
    except:
        pass


try:
    shutil.copy(root+"/libavcodec.so", lib+"/libavcodec.so.60")
except:
    pass

try:
    shutil.copy(root+"/libavformat.so", lib+"/libavformat.so.60")
except:
    pass

try:
    shutil.copy(root+"/libavutil.so", lib+"/libavutil.so.58")
except:
    pass

try:
    shutil.copy(root+"/libswscale.so", lib+"/libswscale.so.7")
except:
    pass

try:
    shutil.copy(root+"/libjpeg.so", lib+"/libjpeg.so.8")
except:
    pass

try:
    shutil.copy(root+"/libswresample.so", lib+"/libswresample.so.4")
except:
    pass

try:
    shutil.copy(root+"/libvpx.so", lib+"/libvpx.so.9")
except:
    pass

try:
    shutil.copy(root+"/libtheoraenc.so", lib+"/libtheoraenc.so.1")
except:
    pass

try:
    shutil.copy(root+"/libtheoradec.so", lib+"/libtheoradec.so.1")
except:
    pass

try:
    shutil.copy(root+"/libvo-amrwbenc.so", lib+"/libvo-amrwbenc.so.0")
except:
    pass

try:
    shutil.copy(root+"/libxvidcore.so", lib+"/libxvidcore.so.4")
except:
    pass

try:
    shutil.copy(root+"/libx264.so", lib+"/libx264.so.164")
except:
    pass

p2 = os.environ['HOME']
p6 = p2+'/lib/'
p7 = '/system/lib64/'
if os.path.exists(p7):
    for i in os.listdir(p7):
        p=p6+i
        if os.path.exists(p):
            os.remove(p)
            print('  remove old '+i+' and relinking new')
        else:
            print('  linking '+i)
        i=p7+i
        #os.symlink(i,p)
        #print('linked'+': %s --> %s'%(i,p))
