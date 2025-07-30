from .libbarpy import *  # Import symbols from the .pyd file
import numpy as np


def append_line_to_matrix(barline : Barline, matrix : np.array):
	ksize = barline.getMatrixSize()
	for i in range(ksize):
		p = barline.getMatrixValue(i)
		matrix[p.y,p.x] += p.value.value()

def combine_components_into_matrix(barlines : list[Barline] | Barline, shape : tuple, imgType = np.uint8):

	if isinstance(barlines, Barline):
		barlines = [barlines]

	binmap = np.zeros(shape, imgType)

	# isRgb = len(shape) == 3
	for bl in barlines:
		append_line_to_matrix(bl, binmap)

	return binmap


class Barcode:
	def __init__(self, img : np.ndarray, build_options : barstruct = barstruct()):
		self.shape = img.shape
		self.imgType = img.dtype
		self.item = create(img, build_options)
		self.revert = build_options.proctype == ProcType.f255t0
		pass

	def get_largest_component(self):
		biggestMatrixId = 0
		lines = self.item.getBarcodeLines()
		msize = lines[0].getMatrixSize()
		for i in range(1, len(lines)):
			if lines[i].getMatrixSize() > msize:
				biggestMatrixId = i
				msize = lines[i].getMatrixSize()

		return lines[biggestMatrixId]

	def get_first_component(self):
		bar = self.item.getBarcodeLines()
		return bar[0]

	def get_first_component_points(self):
		bar = self.item.getBarcodeLines()
		if len(bar) > 0:
			return np.array(self.item.getBarcodeLines()[0].getPoints())
		else:
			return np.array([])

	def restore(self):
		binmap = combine_components_into_matrix(self.item.getBarcodeLines(), self.shape, self.imgType)

		if not self.revert:
			binmap = 255 - binmap

		return binmap

	def getComponents(self) -> set[Barline]:
		return self.item.getBarcodeLines()

	def split_components(self, threshold : int) -> tuple[np.array, np.array]:
		if threshold > len(self.item.getBarcodeLines()):
			a = combine_components_into_matrix(self, self.item.getBarcodeLines(), self.shape, self.imgType)
			b = np.zeros(self.shape, self.imgType)
			return (a, b)

		a = self.item.getBarcodeLines()[:threshold]
		b = self.item.getBarcodeLines()[threshold:]
		a = combine_components_into_matrix(self, a, self.shape, self.imgType)
		b = combine_components_into_matrix(self, b, self.shape, self.imgType)
		return (a, b)

	def combine_components_into_matrix(self):
		return combine_components_into_matrix(self.item.getBarcodeLines(), self.shape, self.imgType)

	def filter(self, LL = 180):
		bar = self.item.getBarcodeLines()

		binmap = np.zeros(self.shape, np.uint8)
		for bl in bar:

			if bl.len() < LL:
				continue

			append_line_to_matrix(bl, binmap)

		if not self.revert:
			binmap = 255 - binmap

		return binmap

	def segmentation(self, useBinarySegment = True):
		bar = self.item.getBarcodeLines()

		# red=(0,0,255)
		# blue =(255,0,0)
		# green=(0,255,0)
		# colors=[red, blue, green]

		from random import randint
		colors = []
		if not useBinarySegment:
			for i in range(len(bar)):
				colors.append(np.array([randint(0, 255),randint(0, 255),randint(0, 255)]))

			binmap = np.zeros((self.shape[0],self.shape[1],3), np.uint8)
		else:
			binmap = np.zeros((self.shape[0],self.shape[1]), np.uint8)

		i=0
		for bl in bar:
			keyvals = bl.getPoints()

			if bl.len() < 40: #and len(keyvals)<500:
				continue

			if (len(keyvals)>self.shape[0]*self.shape[1]*0.9):
				continue

			for p in keyvals:
				binmap[p.y,p.x] = 255 if useBinarySegment else colors[i%len(colors)]

			i+=1

		return binmap



def create_barcode(img, struct : barstruct):
	return Barcode(img, struct)
