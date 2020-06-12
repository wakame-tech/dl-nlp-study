# https://stackoverflow.com/questions/60478862/how-to-avoid-runtimeerror-error-in-loadlibrarya-for-torch-cat
import ctypes
ctypes.cdll.LoadLibrary('caffe2_nvrtc.dll')
