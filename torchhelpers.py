import torch
from torch.autograd import Variable

class linearRegression(torch.nn.Module):
    def __init__(self, inputSize, outputSize):
        super(linearRegression, self).__init__()
        self.linear = torch.nn.Linear(inputSize, outputSize)

    def forward(self, x):
        out = self.linear(x)
        return out

# least square loss
def ls(r):
    return (1-r)**2

inputDim = 1        # takes variable 'x' 
outputDim = 1       # takes variable 'y'
learningRate = 0.00001 
epochs = 1000

models = []
for i in range(y_classes_num):
    models.append(linearRegression(inputDim, outputDim))

def OVA_loss(outputs, labels):
    loss = 0
    for i in range(len(labels)):
        loss += ls(outputs[int(labels[i])][i])
        for j in range(y_classes_num):
            if j != int(labels[i]):
                loss += ls(-outputs[j][i])
    return loss


##### For GPU #######
if torch.cuda.is_available():
    for m in models:
        m.cuda()

criterion = torch.nn.MSELoss() 

optimizers = []
for m in models:
    optimizers.append(torch.optim.SGD(m.parameters(), lr=learningRate))

for epoch in range(epochs):
    # Converting inputs and labels to Variable
    if torch.cuda.is_available():
        inputs = Variable(torch.from_numpy(x_train).cuda())
        labels = Variable(torch.from_numpy(y_train).cuda())
    else:
        inputs = Variable(torch.from_numpy(x_train))
        labels = Variable(torch.from_numpy(y_train))

    # Clear gradient buffers because we don't want any gradient from previous epoch to carry forward, dont want to cummulate gradients
    for o in optimizers:
        o.zero_grad()

    # get output from the model, given the inputs
    outputs = []
    for m in models:
        outputs.append(m(inputs))

    # get loss for the predicted output
    loss = OVA_loss(outputs, labels)
    print(loss)
    # get gradients w.r.t to parameters
    loss.backward()

    # update parameters
    for o in optimizers:
        o.step()

    print('epoch {}, loss {}'.format(epoch, loss.item()))