function [theta1, theta2] = gradientDecent(theta1, theta2, learningRate)

% update the parameter
dataSet = [0,0,0 ; 0,1,1 ; 1,0,1 ; 1,1,0];
costValue = 0;
for i = 1:4
	data = dataSet(i,:);
	x = data(1,1);
	y = data(1,2);
	target = data(1,3);

	[forwardLayer1, forwardLayer2, forwardLayer3] = 
		neuralNetwork([x,y], theta1, theta2);
	j_D_a3 = -(target - forwardLayer3);
	a3_D_z3 = forwardLayer3 * (1 - forwardLayer3);
	z3_D_theta3 = forwardLayer2;
	gredient2 = j_D_a3 * a3_D_z3 * z3_D_theta3;
	delta3 = j_D_a3 * a3_D_z3;

	j_D_a2 = j_D_a3 * a3_D_z3 * theta2;
	j_D_a2 = j_D_a2(2:3);
	a2_D_z2 = forwardLayer2' .* (1 - forwardLayer2');
	a2_D_z2 = a2_D_z2(2:3);
	delta2 = j_D_a2 .* a2_D_z2;
	gredient11 = forwardLayer1' * delta2(1);
	gredient12 = forwardLayer1' * delta2(2);
	gredient1 = [gredient11, gredient12];
	costValue = costValue + 0.5 * (target - forwardLayer3) ** 2;

	theta1 = theta1 - learningRate * gredient1;
	theta2 = theta2 - learningRate * gredient2';
end
costValue