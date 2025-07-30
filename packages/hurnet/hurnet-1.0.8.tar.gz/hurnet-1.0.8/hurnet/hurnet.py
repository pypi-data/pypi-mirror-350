"""
    ############################################################################################################################################################################################################################
    # This algorithm represents a revolutionary new architecture of artificial neural networks created by Sapiens Technology®, which is significantly faster and more accurate than conventional neural network architectures. #
    # The HurNet network, which uses back-division calculations where the computation starts from the output layer and goes back to the previous layers up to the input layer,                                                 #
    # dividing each current neuron by the immediately previous one in a single iteration,                                                                                                                                      #
    # manages to be significantly faster than traditional neural networks that use several iterations of weight adjustment through backpropagation.                                                                            #
    # The neural network architecture in question has been named HurNet (Hur, from Ben-Hur Varriano, who designed the mathematical architecture and the network algorithm; and Net, from neural network).                      #
    # The HurNet neural network does not rely on backpropagation or gradient calculations, achieving optimal weight adjustments in a single iteration.                                                                         #
    # This approach dramatically reduces demands for computational processing and can potentially increase training speed.                                                                                                     #
    # This algorithm is protected by copyright, and any public commentary, disclosure, or distribution of the HurNet algorithm code without prior authorization from Sapiens Technology® is strictly prohibited.               #
    # Reverse engineering and the creation of derivative algorithms through adaptations or inspirations based on the original calculations and code are also not allowed.                                                      #
    # Any violation of these prohibitions will be subject to legal action by our legal department.                                                                                                                             #
    ############################################################################################################################################################################################################################
"""
class HurNet:
	def __init__(self, architecture='multi_layer', fx=True):
		try:
			architecture = architecture.lower().strip() if type(architecture) == str else str(architecture).lower().strip()
			fx = bool(fx) if type(fx) in (bool, int, float) else True
			if architecture == 'multi_layer' and fx: from hurnet._hurnet import MultiLayerHurNetFX as HUR_NET
			elif architecture == 'single_layer' and fx: from hurnet._hurnet import SingleLayerHurNetFX as HUR_NET
			elif architecture == 'multi_layer' and not fx: from hurnet._hurnet import MultiLayerHurNet as HUR_NET
			elif architecture == 'single_layer' and not fx: from hurnet._hurnet import SingleLayerHurNet as HUR_NET
			else: from hurnet._hurnet import MultiLayerHurNetFX as HUR_NET
			self.__architecture, self.__fx, self.__HUR_NET = architecture, fx, HUR_NET()
		except Exception as error: print('ERROR in HurNet.__init__: ' + str(error))
	def addHiddenLayer(self, num_neurons=1):
		try:
			HUR_NET = None
			if not self.__architecture.startswith('multi') and self.__fx: from hurnet._hurnet import MultiLayerHurNetFX as HUR_NET
			elif not self.__architecture.startswith('multi') and not self.__fx: from hurnet._hurnet import MultiLayerHurNet as HUR_NET
			if HUR_NET is not None: self.__HUR_NET = HUR_NET()
			return self.__HUR_NET.addHiddenLayer(num_neurons=num_neurons)
		except Exception as error:
			print('ERROR in HurNet.addHiddenLayer: ' + str(error))
			return False
	def train(self, input_layer=[], output_layer=[], interaction=True, activation_function='linear', bias=0, learning_rate=1, stochastic_factor=False):
		try:
			learning_rate = float(learning_rate) if type(learning_rate) in (bool, int, float) else 1
			stochastic_factor = bool(stochastic_factor) if type(stochastic_factor) in (bool, int, float) else False
			train_return = self.__HUR_NET.train(input_layer=input_layer, output_layer=output_layer, interaction=interaction,
			activation_function=activation_function, bias=bias)
			if learning_rate != 1: self.__HUR_NET._weights = self.__HUR_NET._weights * learning_rate
			if stochastic_factor:
				from numpy import random, min, max
				def adds_randomness(array_x=[], minimum_limit=0, maximum_limit=1):
					random_values = random.rand(*array_x.shape) * (maximum_limit - minimum_limit) + minimum_limit
					return array_x + random_values
				minimum_limit, maximum_limit = min(self.__HUR_NET._weights) * -1, max(self.__HUR_NET._weights)
				self.__HUR_NET._weights = adds_randomness(array_x=self.__HUR_NET._weights, minimum_limit=minimum_limit, maximum_limit=maximum_limit)
			return train_return
		except Exception as error:
			print('ERROR in HurNet.train: ' + str(error))
			return False
	def saveModel(self, model_path=''):
		try: return self.__HUR_NET.saveModel(model_path=model_path)
		except Exception as error:
			print('ERROR in HurNet.saveModel: ' + str(error))
			return False
	def loadModel(self, model_path=''):
		try: return self.__HUR_NET.loadModel(model_path=model_path)
		except Exception as error:
			print('ERROR in HurNet.loadModel: ' + str(error))
			return False
	def predict(self, input_layer=[], decimal_places=8):
		try: return self.__HUR_NET.predict(input_layer=input_layer, decimal_places=decimal_places)
		except Exception as error:
			print('ERROR in HurNet.predict: ' + str(error))
			return False
def measure_execution_time(function=print, display_message=True, *args, **kwargs):
	from hurnet._hurnet import measure_execution_time
	return measure_execution_time(function, display_message)
def tensor_similarity_percentage(obtained_output=[], expected_output=[]):
	from hurnet._hurnet import tensor_similarity_percentage
	return tensor_similarity_percentage(obtained_output=obtained_output, expected_output=expected_output)
"""
    ############################################################################################################################################################################################################################
    # This algorithm represents a revolutionary new architecture of artificial neural networks created by Sapiens Technology®, which is significantly faster and more accurate than conventional neural network architectures. #
    # The HurNet network, which uses back-division calculations where the computation starts from the output layer and goes back to the previous layers up to the input layer,                                                 #
    # dividing each current neuron by the immediately previous one in a single iteration,                                                                                                                                      #
    # manages to be significantly faster than traditional neural networks that use several iterations of weight adjustment through backpropagation.                                                                            #
    # The neural network architecture in question has been named HurNet (Hur, from Ben-Hur Varriano, who designed the mathematical architecture and the network algorithm; and Net, from neural network).                      #
    # The HurNet neural network does not rely on backpropagation or gradient calculations, achieving optimal weight adjustments in a single iteration.                                                                         #
    # This approach dramatically reduces demands for computational processing and can potentially increase training speed.                                                                                                     #
    # This algorithm is protected by copyright, and any public commentary, disclosure, or distribution of the HurNet algorithm code without prior authorization from Sapiens Technology® is strictly prohibited.               #
    # Reverse engineering and the creation of derivative algorithms through adaptations or inspirations based on the original calculations and code are also not allowed.                                                      #
    # Any violation of these prohibitions will be subject to legal action by our legal department.                                                                                                                             #
    ############################################################################################################################################################################################################################
"""
