% main function
learningRate = 0.3;
ECHO = 3000;
theta1 = rand(3,2);
theta2 = rand(3,1);
% theta1 = [-30, 10; 20, -20; 20, -10] % fixed parameter
% theta2 = [-10; 20; 20]               % fixed parameter
for i = 1:ECHO
	[theta1, theta2] = gradientDecent(theta1, theta2, learningRate);
end

% Here we begin test
dataSet = [0,0,0 ; 0,1,1 ; 1,0,1 ; 1,1,0]
target = [0;1;1;0]
[layer1, layer2, layer3] = neuralNetwork([0,0], theta1, theta2);
layer3
[layer1, layer2, layer3] = neuralNetwork([0,1], theta1, theta2);
layer3
[layer1, layer2, layer3] = neuralNetwork([1,0], theta1, theta2);
layer3
[layer1, layer2, layer3] = neuralNetwork([1,1], theta1, theta2);
layer3
