import nibabel
import vtk


vol = nibabel.load('t1_brain_mask.nii.gz')

im_data = vol.get_data().tostring()
img = vtk.vtkImageImport()
img.CopyImportVoidPointer(im_data, len(im_data))
img.SetDataScalarType(vtk.VTK_UNSIGNED_SHORT)
img.SetNumberOfScalarComponents(1)
img.SetDataExtent(0, vol.shape[2]-1, 0, vol.shape[1]-1, 0, vol.shape[0]-1)
img.SetWholeExtent(0, vol.shape[2]-1, 0, vol.shape[1]-1, 0, vol.shape[0]-1)

iso = vtk.vtkMarchingCubes()
iso.SetInput(img.GetOutput())
iso.SetValue(0,1)
#120 vessles near cerebellum
#100 cortex
#20 face
#iso SetStartMethod {puts "Start Marching"}

isoMapper = vtk.vtkPolyDataMapper()
isoMapper.SetInput(iso.GetOutput())
isoMapper.ScalarVisibilityOff()

isoActor = vtk.vtkActor()
isoActor.SetMapper(isoMapper)
isoActor.GetProperty().SetColor([1.,1.,.9])

outline = vtk.vtkOutlineFilter()
outline.SetInput(img.GetOutput())
outlineMapper = vtk.vtkPolyDataMapper()
outlineMapper.SetInput(outline.GetOutput())
outlineActor = vtk.vtkActor()
outlineActor.SetMapper(outlineMapper)
outlineActor.VisibilityOff()

ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
# Add the actors to the renderer, set the background and size
#
ren.AddActor(outlineActor)
ren.AddActor(isoActor)
ren.SetBackground(0.2,0.3,0.4)
renWin.SetSize(450,450)
## ren.GetActiveCamera().Elevation(235)
## ren.GetActiveCamera().SetViewUp(0,.5,-1)
## ren.GetActiveCamera().Azimuth(90)


iren.Initialize()

iren.Start()

