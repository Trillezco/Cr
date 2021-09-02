import Functions as F


# images="/home/gonzatrille/Escritorio/Universidad/Tesis/My Algorithm/Histogram/narrow/centimeter/**"
# images="/home/gonzatrille/Escritorio/Universidad/Tesis/My Algorithm/Histogram/narrow/parsec/**"
# images= "/home/gonzatrille/Escritorio/Universidad/Tesis/My Algorithm/Histogram/wide/centimeter/**"
# images="/home/gonzatrille/Escritorio/Universidad/Tesis/My Algorithm/Histogram/wide/parsec/**"
# images= "/home/gonzatrille/Escritorio/Universidad/Tesis/My Algorithm/kde/parsec/**"
# images= "/home/gonzatrille/Escritorio/Universidad/Tesis/My Algorithm/kde/centimeter/**"
images= "/home/gonzatrille/Escritorio/Universidad/Tesis/My Algorithm/kde/centimeter (copia)/**"

images= "/home/gonzatrille/Escritorio/Universidad/Tesis/My Algorithm/kde/centimeter"

Animator(images)

files = glob.glob(images)
files=natsort.natsorted(files)

Image = []
for File in files:
	Image.append(imageio.imread(File))
imageio.mimsave('KDENarrowCentimeterOtro.gif', Image, fps=10, duration=0.2)


def Animator(Root):
	plots = glob.glob(Root+"/**")
	plots = natsort.natsorted(plots)	;	List = []
	for Plot in plots:
		List.append(imageio.imread(Plot))
	imageio.mimsave("Animation.gif", List, fps=10, duration=0.2)
	return
