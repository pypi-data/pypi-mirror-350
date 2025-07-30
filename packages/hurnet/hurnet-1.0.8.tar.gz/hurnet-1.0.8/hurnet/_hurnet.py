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
class __HurNet:
    def __init__(self):
        try:
            from warnings import filterwarnings
            from numpy import ndarray, isscalar, array, exp, tanh, maximum, where, max, sum, log, clip, mean, linalg, argmin, round, prod, hstack, ones
            from random import random
            from numpy.linalg import pinv
            from pickle import dump, load
            from os import path
            filterwarnings('ignore')
            self._ndarray = ndarray
            self._isscalar = isscalar
            self._array = array
            self._exp = exp
            self._tanh = tanh
            self._maximum = maximum
            self._where = where
            self._max = max
            self._sum = sum
            self._log = log
            self._clip = clip
            self._mean = mean
            self._linalg = linalg
            self._argmin = argmin
            self._round = round
            self._prod = prod
            self._hstack = hstack
            self._ones = ones
            self._random = random
            self._pinv = pinv
            self._dump = dump
            self._path = path
            self._load = load
            self._one_dimensional_output = False
            self._weights = None
            self._output_sample_shape = None
            self._input_layer = None
            self._output_shape = []
            self._activation = 'linear'
            self._y_is_1d = False
            self._y_shape = None
            self._interaction = True
            self._num_hidden_layers = 0                
        except Exception as error: print('ERROR in class __HurNet.__init__: ' + str(error))
    def _integer_validation(self, integer=0): return int(integer) if type(integer) in (bool, int, float) else 0
    def _list_validation(self, x=[], y=None):
        if isinstance(x, self._ndarray): x = x.tolist()
        elif x == []: x = [0]
        else: x = list(x) if type(x) in (tuple, list) else [x]
        if y is not None:
            if isinstance(y, self._ndarray): y = y.tolist()
            elif y == []: y = [0]
            else: y = list(y) if type(y) in (tuple, list) else [y]
            try:
                x_length, y_length = len(x), len(y)
                if x_length != y_length:
                    minimum_length = min((x_length, y_length))
                    x = x[:minimum_length]
                    y = y[:minimum_length]
                if self._isscalar(x[0]): x = [[a] for a in x]
                if self._isscalar(y[0]): y, self._one_dimensional_output = [[b] for b in y], True
            except: pass
            return self._array(x), self._array(y)
        if self._isscalar(x[0]): x = [[a] for a in x]
        return self._array(x)
    def _apply_activation(self, x=[], activation='linear'):
        if activation == 'sigmoid': return 1 / (1 + self._exp(-x))
        elif activation == 'tanh': return self._tanh(x)
        elif activation == 'relu': return self._maximum(0, x)
        elif activation == 'leaky_relu': return self._where(x > 0, x, x * 0.01)
        elif activation == 'softmax':
            exp_x = self._exp(x - self._max(x, axis=1, keepdims=True))
            return exp_x / self._sum(exp_x, axis=1, keepdims=True)
        elif activation == 'softplus': return self._log(1 + self._exp(x))
        elif activation == 'elu': return self._where(x > 0, x, 1.0 * (self._exp(x) - 1))
        elif activation in ('silu', 'swish'): return x * (1 / (1 + self._exp(-x)))
        elif activation == 'gelu': return x * (1 / (1 + self._exp(-1.702 * x)))
        elif activation == 'selu': return 1.05070098 * self._where(x > 0, x, 1.67326324 * (self._exp(x) - 1))
        elif activation == 'mish': return x * self._tanh(self._log(1 + self._exp(x)))
        elif activation == 'hard_sigmoid': return self._clip((x + 3) / 6, 0, 1)
        else: return x
    def _saveModel(self, model_path=''):
        try:
            model_path = model_path.strip() if type(model_path) == str else str(model_path).strip()
            if len(model_path) < 1: model_path = 'model.hurnet'
            if not model_path.lower().endswith('.hurnet'): model_path += '.hurnet'
            if self._weights is None: self._weights = []
            self._output_sample_shape = self._output_sample_shape if type(self._output_sample_shape) in (tuple, list, self._ndarray) else [-1]
            if type(self._output_sample_shape) == tuple: self._output_sample_shape = list(self._output_sample_shape)
            if self._input_layer is None: self._input_layer = []
            self._y_shape = self._y_shape if type(self._y_shape) in (tuple, list, self._ndarray) else [-1]
            if type(self._y_shape) == tuple: self._y_shape = list(self._output_sample_shape)
            if self._y_shape == [-1]: self._y_shape = self._output_sample_shape
            elif self._output_sample_shape == [-1]: self._output_sample_shape = self._y_shape            
            data = {
                'one_dimensional_output': int(self._one_dimensional_output),
                'weights': self._weights.tolist() if hasattr(self._weights, 'tolist') else self._weights,
                'output_sample_shape': self._output_sample_shape.tolist() if hasattr(self._output_sample_shape, 'tolist') else self._output_sample_shape,
                'input_layer': self._input_layer.tolist() if hasattr(self._input_layer, 'tolist') else self._input_layer,
                'output_shape': self._output_shape.tolist() if hasattr(self._output_shape, 'tolist') else self._array(self._output_shape).tolist(),
                'activation': str(self._activation).lower().strip(),
                'y_is_1d': int(self._y_is_1d),
                'y_shape': self._y_shape.tolist() if hasattr(self._y_shape, 'tolist') else self._y_shape,
                'interaction': int(self._interaction),
                'num_hidden_layers': int(self._num_hidden_layers)
            }
            with open(model_path, 'wb') as file: self._dump(data, file)
            return True
        except Exception as error:
            print('ERROR in __HurNet._saveModel: ' + str(error))
            return False
    def _loadModel(self, model_path=''):
        try:
            model_path, data = model_path.strip() if type(model_path) == str else str(model_path).strip(), ''
            if len(model_path) < 1: model_path = 'model.hurnet'
            if not model_path.lower().endswith('.hurnet'): model_path += '.hurnet'
            if not self._path.isfile(model_path): return False
            with open(model_path, 'rb') as file: data = self._load(file)
            def load_model(content=''):
                json_dictionary = {}
                content = str(content)
                try:
                    from json import loads
                    json_dictionary = loads(content)
                except:
                    from ast import literal_eval
                    json_dictionary = literal_eval(content)
                return json_dictionary
            data = load_model(content=data)
            try: self._one_dimensional_output = bool(data['one_dimensional_output'])
            except: self._one_dimensional_output = False
            try: self._weights = self._array(data['weights'])
            except: self._weights = None
            try: self._output_sample_shape = tuple(data['output_sample_shape'])
            except: self._output_sample_shape = None
            try: self._input_layer = self._array(data['input_layer'])
            except: self._input_layer = None
            try: self._output_shape = list(data['output_shape'])
            except: self._output_shape = []
            try: self._activation = str(data['activation']).lower().strip()
            except: self._activation = 'linear'
            try: self._y_is_1d = bool(data['y_is_1d'])
            except: self._y_is_1d = False
            try: self._y_shape = tuple(data['y_shape'])
            except: self._y_shape = None
            try: self._interaction = bool(data['interaction'])
            except: self._interaction = True
            try: self._num_hidden_layers = int(data['num_hidden_layers'])
            except: self._num_hidden_layers = 0
            if self._output_sample_shape == (-1,): self._output_sample_shape = None
            if self._y_shape == (-1,): self._y_shape = None
            return True
        except Exception as error:
            print('ERROR in __HurNet._loadModel: ' + str(error))
            return False
class SingleLayerHurNet(__HurNet):
    def __proximityCalculation(self, input_layer=[]):
        input_flat = self._array(input_layer).flatten()
        input_layer_flat = self._array([x.flatten() for x in self._input_layer])
        differences = input_layer_flat - input_flat
        distances = self._linalg.norm(differences, axis=1)
        return self._argmin(distances)
    def train(self, input_layer=[], output_layer=[], interaction=True, activation_function='linear', bias=0):
        try:
            input_array, output_array = self._list_validation(x=input_layer, y=output_layer)
            interaction = bool(interaction) if type(interaction) in (bool, int, float) else True
            activation = activation_function.lower().strip() if type(activation_function) == str else 'linear'
            bias = float(bias) if type(bias) in (bool, int, float) else 0
            self._output_shape = [self._array(x).shape for x in output_layer]
            input_flat = self._array([self._array(x).flatten() for x in input_layer])
            output_flat = self._array([self._array(x).flatten() for x in output_layer])
            summation_function = self._sum(input_flat, axis=1, keepdims=True)
            summation_function[summation_function == 0] = 1
            weights_per_sample = output_flat / summation_function
            self._weights = self._mean(weights_per_sample, axis=0) if not interaction else weights_per_sample
            self._weights = self._apply_activation(x=self._weights, activation=activation) + bias
            self._input_layer = input_array
            return True
        except Exception as error:
            print(f'ERROR in SingleLayerHurNet.train: ' + str(error))
            self._weights = output_layer
            return False
    def saveModel(self, model_path=''): return self._saveModel(model_path=model_path)
    def loadModel(self, model_path=''): return self._loadModel(model_path=model_path)
    def predict(self, input_layer=[], decimal_places=8):
        try:
            outputs = []
            input_array = self._list_validation(x=input_layer)
            decimal_places = int(decimal_places) if type(decimal_places) in (bool, int, float) else 8
            if self._weights is None:
                print('No training has been carried out yet!!')
                return []
            if len(self._weights.shape) == 1 or (len(self._weights.shape) == 2 and self._weights.shape[0] == 1):
                for inputs in input_array:
                    inputs_flat = self._array(inputs).flatten()
                    summation_function = self._sum(inputs_flat)
                    if summation_function == 0: summation_function = 1
                    output_flat = summation_function * self._array(self._weights)
                    output = output_flat.reshape(tuple(self._output_shape[0]))
                    outputs.append(output)
            else:
                for inputs in input_array:
                    nearest_index = self.__proximityCalculation(inputs)
                    inputs_flat = self._array(inputs).flatten()
                    summation_function = self._sum(inputs_flat)
                    if summation_function == 0: summation_function = 1
                    weights = self._weights[nearest_index]
                    output_flat = summation_function * self._array(weights)
                    output = output_flat.reshape(tuple(self._output_shape[nearest_index]))
                    outputs.append(output)
            outputs = self._round(self._array(outputs), decimal_places).tolist()
            if decimal_places < 1: outputs = self._array(outputs).astype(int).tolist()
            return outputs
        except Exception as error:
            print(f'ERROR in SingleLayerHurNet.predict: ' + str(error))
            try:
                prediction = self._round(self._weights, decimal_places)
                if decimal_places < 1: prediction = self._array(prediction).astype(int)
                return prediction.tolist() if hasattr(prediction, 'tolist') else prediction
            except: return input_layer
class MultiLayerHurNet(__HurNet):
    def __proximityCalculation(self, sample=[]):
        sample = self._array(sample)
        training = self._array(self._input_layer)
        differences = training - sample
        reshaped = differences.reshape(differences.shape[0], -1)
        distances = self._linalg.norm(reshaped, axis=1)
        return self._argmin(distances)
    def addHiddenLayer(self, num_neurons=0):
        try:
            num_neurons = self._integer_validation(num_neurons)
            if num_neurons < 1: return False
            hidden_layer = [self._random() for _ in range(num_neurons)]
            if not hasattr(self, '_hidden_layers'): self._hidden_layers = []
            self._hidden_layers.append(hidden_layer)
            return True
        except Exception as error:
            print('ERROR in MultiLayerHurNet.addHiddenLayer: ' + str(error))
            return False
    def train(self, input_layer=[], output_layer=[], interaction=True, activation_function='linear', bias=0):
        try:
            input_array, output_array = self._list_validation(x=input_layer, y=output_layer)
            interaction = bool(interaction) if type(interaction) in (bool, int, float) else True
            activation = activation_function.lower().strip() if isinstance(activation_function, str) else 'linear'
            bias = float(bias) if type(bias) in (bool, int, float) else 0
            self._output_sample_shape = output_array.shape[1:] if output_array.ndim > 1 else ()
            if input_array.ndim > 1:
                axes = tuple(range(1, input_array.ndim))
                summation_function = self._sum(input_array, axis=axes)
            else: summation_function = self._sum(input_array)
            if isinstance(summation_function, self._ndarray): summation_function = self._where(summation_function == 0, 1, summation_function)
            else:
                if summation_function == 0: summation_function = 1
            n_samples = input_array.shape[0]
            if output_array.ndim > 1:
                reshape_dims = (n_samples,) + (1,) * (output_array.ndim - 1)
                summation_function = summation_function.reshape(reshape_dims)
            weights_per_sample = output_array / summation_function
            if not interaction: self._weights = self._mean(weights_per_sample, axis=0)
            else: self._weights = weights_per_sample
            if hasattr(self, '_hidden_layers') and self._hidden_layers:
                for hidden_layer in self._hidden_layers:
                    avg_hidden = self._mean(hidden_layer)
                    self._weights = self._apply_activation(self._weights + (self._weights * 0.1 * avg_hidden), activation)
            else: self._weights = self._apply_activation(self._weights, activation)
            self._weights = self._weights + bias
            self._input_layer = input_array.tolist()
            return True
        except Exception as error:
            print('ERROR in MultiLayerHurNet.train: ' + str(error))
            self._weights = output_layer
            return False
    def saveModel(self, model_path=''): return self._saveModel(model_path=model_path)
    def loadModel(self, model_path=''): return self._loadModel(model_path=model_path)
    def predict(self, input_layer=[], decimal_places=8):
        try:
            input_array = self._list_validation(x=input_layer)
            decimal_places = int(decimal_places) if type(decimal_places) in (bool, int, float) else 8
            if self._weights is None:
                print('No training has been carried out yet!')
                return input_layer
            n_samples = input_array.shape[0]
            if input_array.ndim > 1:
                axes = tuple(range(1, input_array.ndim))
                summation_function = self._sum(input_array, axis=axes)
            else: summation_function = self._sum(input_array)
            output_list = []
            single_weight = (hasattr(self._weights, 'ndim') and (self._weights.ndim == len(self._output_sample_shape) or self._weights.ndim == 0))
            for index in range(n_samples):
                if single_weight: weight = self._weights
                else: weight = self._weights[self.__proximityCalculation(input_array[index])]
                prediction = summation_function[index] * weight
                prediction = self._round(prediction, decimal_places)
                if decimal_places < 1: prediction = self._array(prediction).astype(int)
                if self._output_sample_shape == () or self._output_sample_shape is None:
                    try: prediction_out = prediction.item()
                    except: prediction_out = prediction
                else: prediction_out = prediction.tolist()
                output_list.append(prediction_out)
            if self._one_dimensional_output: output_list = [output[0] for output in output_list]
            return output_list
        except Exception as error:
            print('ERROR in MultiLayerHurNet.predict: ' + str(error))
            try:
                prediction = self._round(self._weights, decimal_places)
                if decimal_places < 1: prediction = self._array(prediction).astype(int)
                return prediction.tolist() if hasattr(prediction, 'tolist') else prediction
            except: return input_layer
class SingleLayerHurNetFX(__HurNet):
    def __add_features(self, x=[], activation='linear'):
        if x.ndim > 2: x = x.reshape(x.shape[0], -1)
        elif x.ndim == 1: x = x.reshape(-1, 1)
        interaction = self._prod(x, axis=1).reshape(-1, 1)
        x = self._hstack([x, interaction, self._ones((x.shape[0], 1))])
        if activation not in ('linear', 'softmax'): x = self._apply_activation(x=x, activation=activation)
        return x
    def train(self, input_layer=[], output_layer=[], interaction=True, activation_function='linear', bias=0):
        try:
            x, y = self._list_validation(x=input_layer, y=output_layer)
            interaction = bool(interaction) if type(interaction) in (bool, int, float) else True
            activation = activation_function.lower().strip() if type(activation_function) == str else 'linear'
            bias = float(bias) if type(bias) in (bool, int, float) else 0
            x, y = self._array(x), self._array(y)
            x_augmented = self.__add_features(x=x, activation=activation)
            self._y_is_1d, self._activation = (y.ndim == 1), activation
            if y.ndim > 2:
                self._y_shape = y.shape[1:]
                y = y.reshape(y.shape[0], -1)
            elif y.ndim == 1:
                self._y_shape = None
                y = y.reshape(-1, 1)
            else: self._y_shape = y.shape[1:] if y.shape[1:] != () else None
            x_augmented_transposed = x_augmented.T
            if not interaction: self._weights = (self._pinv(x_augmented) @ y) + bias
            else: self._weights = (self._pinv(x_augmented_transposed @ x_augmented) @ (x_augmented_transposed @ y)) + bias
            return True
        except Exception as error:
            print('ERROR in SingleLayerHurNetFX.train: ' + str(error))
            self._weights = output_layer
            return False
    def saveModel(self, model_path=''): return self._saveModel(model_path=model_path)
    def loadModel(self, model_path=''): return self._loadModel(model_path=model_path)
    def predict(self, input_layer=[], decimal_places=8):
        try:
            x = self._list_validation(x=input_layer)
            decimal_places = int(decimal_places) if type(decimal_places) in (bool, int, float) else 8
            x = self._array(x)
            x_augmented = self.__add_features(x=x, activation=self._activation)
            predictions = x_augmented @ self._weights
            if self._activation == 'softmax': predictions = self._apply_activation(predictions, 'softmax')
            if decimal_places < 1: predictions = self._round(predictions).astype(int)
            else: predictions = self._round(predictions, decimal_places).astype(float)
            if self._y_shape is not None:
                result = []
                for prediction in predictions: result.append(self._array(prediction).reshape(self._y_shape).tolist())
                predictions = result
            elif self._y_is_1d: predictions = predictions.flatten().tolist()
            else: predictions = predictions.tolist()
            if self._one_dimensional_output: predictions = [output[0] for output in predictions]
            return predictions
        except Exception as error:
            print('ERROR in SingleLayerHurNetFX.predict: ' + str(error))
            try:
                predictions = self._weights
                if decimal_places < 1: predictions = self._round(predictions).astype(int)
                else: predictions = self._round(predictions, decimal_places).astype(float)
                return predictions.tolist() if hasattr(predictions, 'tolist') else predictions
            except: return input_layer
class MultiLayerHurNetFX(__HurNet):
    def __add_features(self, x=[], interaction=True, activation='linear'):
        if x.ndim > 2: x = x.reshape(x.shape[0], -1)
        elif x.ndim == 1: x = x.reshape(-1, 1)
        if interaction:
            interaction_x = self._prod(x, axis=1).reshape(-1, 1)
            x = self._hstack([x, interaction_x, self._ones((x.shape[0], 1))])
        else: x = self._hstack([x, self._ones((x.shape[0], 1))])
        if activation not in ('linear', 'softmax'): x = self._apply_activation(x=x, activation=activation)
        return x
    def __fit(self, x=[], y=[], interaction=True, activation='linear', bias=0):
        x_augmented = x.copy()
        for _ in range(self._num_hidden_layers + 1): x_augmented = self.__add_features(x=x_augmented, interaction=interaction, activation=activation)
        self._y_is_1d = (y.ndim == 1)
        x_augmented_transposed = x_augmented.T
        if interaction: self._weights = (self._pinv(x_augmented) @ y) + bias
        else: self._weights = (self._pinv(x_augmented_transposed @ x_augmented) @ (x_augmented_transposed @ y)) + bias
    def addHiddenLayer(self, num_neurons=1):
        try:
            number_of_neurons = self._integer_validation(integer=num_neurons)
            self._num_hidden_layers += number_of_neurons
            return True
        except Exception as error:
            print('ERROR in MultiLayerHurNetFX.addHiddenLayer: ' + str(error))
            return False
    def train(self, input_layer=[], output_layer=[], interaction=True, activation_function='linear', bias=0):
        try:
            x, y = self._list_validation(x=input_layer, y=output_layer)
            interaction = bool(interaction) if type(interaction) in (bool, int, float) else True
            activation = activation_function.lower().strip() if type(activation_function) == str else 'linear'
            bias = float(bias) if type(bias) in (bool, int, float) else 0
            x, y = self._array(x), self._array(y)
            if y.ndim > 2:
                self._y_shape = y.shape[1:]
                y = y.reshape(y.shape[0], -1)
            elif y.ndim == 1:
                self._y_shape = None
                y = y.reshape(-1, 1)
            else: self._y_shape = y.shape[1:] if y.shape[1:] != () else None
            self._interaction, self._activation = interaction, activation
            try: self.__fit(x=x, y=y, interaction=self._interaction, activation=activation, bias=bias)
            except:
                self._num_hidden_layers = 0
                self._interaction = False
                self.__fit(x, y, interaction=self._interaction, activation=activation, bias=bias)
            return True
        except Exception as error:
            print('ERROR in MultiLayerHurNetFX.train: ' + str(error))
            self._weights = output_layer
            return False
    def saveModel(self, model_path=''): return self._saveModel(model_path=model_path)
    def loadModel(self, model_path=''): return self._loadModel(model_path=model_path)
    def predict(self, input_layer=[], decimal_places=8):
        try:
            x = self._list_validation(x=input_layer)
            decimal_places = int(decimal_places) if type(decimal_places) in (bool, int, float) else 8
            x, number_of_hidden_layers = self._array(x), self._num_hidden_layers
            x_augmented = x.copy()
            for _ in range(number_of_hidden_layers + 1): x_augmented = self.__add_features(x_augmented, interaction=self._interaction)
            predictions = x_augmented @ self._weights
            if self._activation == 'softmax': predictions = self._apply_activation(predictions, 'softmax')
            if decimal_places < 1: predictions = self._round(predictions).astype(int)
            else: predictions = self._round(predictions, decimal_places).astype(float)
            if self._y_shape is not None:
                result = []
                for prediction in predictions: result.append(self._array(prediction).reshape(self._y_shape).tolist())
                predictions = result
            elif self._y_is_1d: predictions = predictions.flatten().tolist()
            else: predictions = predictions.tolist()
            if self._one_dimensional_output: predictions = [output[0] for output in predictions]
            return predictions
        except Exception as error:
            print('ERROR in MultiLayerHurNetFX.predict: ' + str(error))
            try:
                predictions = self._weights
                if decimal_places < 1: predictions = self._round(predictions).astype(int)
                else: predictions = self._round(predictions, decimal_places).astype(float)
                return predictions.tolist() if hasattr(predictions, 'tolist') else predictions
            except: return input_layer
def measure_execution_time(function=print, display_message=True, *args, **kwargs):
    try:
        display_message = bool(display_message) if type(display_message) in (bool, int, float) else True
        from time import perf_counter
        start = perf_counter()
        result = function(*args, **kwargs)
        end = perf_counter()
        execution_time = abs(end - start)
        if display_message: print(f'Execution time: {execution_time:.10f} seconds.')
        return execution_time
    except Exception as error:
        print('ERROR in measure_execution_time: ' + str(error))
        return 1
def tensor_similarity_percentage(obtained_output=[], expected_output=[]):
    try:
        from numpy import array, maximum, mean, where
        obtained_output = array(obtained_output)
        expected_output = array(expected_output)
        if obtained_output.shape != expected_output.shape: return 0
        difference = abs(obtained_output - expected_output)
        greatest_value = maximum(obtained_output, expected_output)
        greatest_value = where(greatest_value == 0, 1, greatest_value)
        quotient = difference / greatest_value
        average = min((1, max((0, mean(quotient)))))
        return 1 - average
    except Exception as error:
        print('ERROR in tensor_similarity_percentage: ' + str(error))
        return 0
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
