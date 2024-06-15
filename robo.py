from roboflow import Roboflow
rf = Roboflow(api_key="3v5l9pg9KLXoKLB928EO")
project = rf.workspace("airborne-object-detection").project("airborne-object-detection-4-aod4")
version = project.version(6)
dataset = version.download("yolov9")
