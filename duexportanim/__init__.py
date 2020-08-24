import krita
from .exportanim import ExportAnimExtension

Scripter.addExtension(ExportAnimExtension(krita.Krita.instance()))
