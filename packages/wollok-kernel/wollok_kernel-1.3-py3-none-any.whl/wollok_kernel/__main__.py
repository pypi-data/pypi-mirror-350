from ipykernel.kernelapp import IPKernelApp
from . import WollokKernel

IPKernelApp.launch_instance(kernel_class=WollokKernel)