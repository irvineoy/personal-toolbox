function [forwardLayer1, forwardLayer2, forwardLayer3] = neuralNetwork(x, theta1, theta2)

% Neural network construction

forwardLayer1 = [1, x];
forwardLayer2 = forwardLayer1 * theta1;
forwardLayer2 = sigmoid(forwardLayer2);
forwardLayer2 = [1, forwardLayer2];
forwardLayer3 = forwardLayer2 * theta2;
forwardLayer3 = sigmoid(forwardLayer3);
