import tensorflow as tf
from tensorflow import keras
from keras.layers import Dense, Input, Conv1D, Conv2D, Conv3D, MaxPooling2D, Flatten, BatchNormalization, concatenate, Dropout, Activation
from keras.optimizers import Adam, SGD, Nadam, Adamax, Adagrad
from keras.models import Model, load_model
from keras.callbacks import TensorBoard, ModelCheckpoint
from keras.utils import plot_model
from matplotlib import pyplot as plt
import numpy as np
import talos


# translate chosen action (array) to joystick action (dict)


def imitation_learning(heat_maps, actions, hist_size, nn_size, batch_size, lr, epochs, new_model = True, train = True ):

    # eval_index = np.random.randint(len(actions), size=int(len(actions)*evals))
    # eval_actions = actions[eval_index]
    # eval_heat_maps = heat_maps[eval_index].reshape(len(eval_index),1,100,6)
    #
    # actions = np.delete(actions, eval_index, axis=0)
    # heat_maps = np.delete(heat_maps, eval_index, axis=0)


    if new_model:   ## create new sequential keras model

        heat_maps = heat_maps.reshape(len(heat_maps), hist_size, 100, 6)

        # hmap_size = heat_maps[0].reshape(1,100,6).shape
        hmap_size = heat_maps.shape[1:]

        ac_size = actions[0].shape[0]

        hmap_input = Input(shape=hmap_size, name='Heat_map_input')

        conv_l = hmap_input

        conv_l = Conv2D(filters=8, kernel_size=(2, 2), strides=(1, 1), padding='same')(conv_l)
        # conv_l = Activation('elu')(conv_l)
        # conv_l = BatchNormalization()(conv_l)
        conv_l = Dropout(rate=0.0)(conv_l)
        conv_l = Conv2D(filters=8, kernel_size=(2, 2), strides=(1, 1), padding='same')(conv_l)
        conv_l = Conv2D(filters=8, kernel_size=(2, 2), strides=(1, 1), padding='same')(conv_l)
        conv_l = Conv2D(filters=64, kernel_size=(4, 4), strides=(1, 1), padding='same')(conv_l)
        conv_l = Dropout(rate=0.0)(conv_l)
        # conv_l = Activation('elu')(conv_l)
        # conv_l = BatchNormalization()(conv_l)
        # conv_l = Dropout(rate=0.1)(conv_l)
        # conv_l = Conv2D(filters=16, kernel_size=(3, 3), strides=(1, 1), padding='same', activation='relu')(conv_l)
        # conv_l = BatchNormalization()(conv_l)
        # conv_l = Conv2D(filters=32, kernel_size=(3, 3), strides=(1, 1), padding='same', activation='relu')(conv_l)
        # conv_l = BatchNormalization()(conv_l)

        conv_l = Flatten()(conv_l)

        # fc_l = concatenate([conv_l, sens_input])
        fc_l = conv_l
        for i in range(len(nn_size)):
            fc_l = Dense(nn_size[i], activation='relu')(fc_l)

        output = Dense(ac_size, activation='relu', use_bias=True)(fc_l)

        model = Model(inputs=hmap_input, outputs=output)

        opt = Adam(lr=lr)
        # opt = Nadam(lr=lr)
        # opt = SGD(lr=lr)

        model.compile(
            loss='mean_absolute_error',
            optimizer=opt)

        print(model.summary())

        # test_name = 'keras_test_1'
        # log_dir = '/home/graphics/git/SmartLoader/log_dir/' + test_name + '/'
        # tensorboard_callback = keras.callbacks.TensorBoard(log_dir=log_dir)

    else:   ### load existing sequential model
       model = load_model('/home/graphics/git/SmartLoader/saved_models/Heatmap/test_model')

    if train:   ## train new agent
        hist = model.fit(
            x=heat_maps,
            y=actions,
            batch_size=batch_size,
            verbose=2,
            epochs=epochs,
            validation_split=0.2
        )
        model.save('/home/graphics/git/SmartLoader/saved_models/Heatmap/test_model')

    x = range(0, epochs)
    plt.plot(x, hist.history['loss'], label="Training Loss")
    plt.plot(x, hist.history['val_loss'], label="Eval Loss")
    plt.xlabel('Epochs')
    plt.ylabel('Loss Value')
    plt.legend(loc="upper left")
    plt.grid(True)
    plt.show()


    print(' ------------ now lets evaluate -------------')

    # loss = []
    # for k in range(len(eval_actions)):
    #     action = model.predict(eval_heat_maps[k].reshape(1,1,100,6))
    #     loss.append(np.abs(action - eval_actions[k]))
    # avg_loss = np.mean(loss)
    # print('avarage loss for {} evaluations: {}'.format(len(eval_actions),avg_loss))
    #



###########  labels[550]  #####  model.predict(states[550].reshape([1,ob_size]))
def main():

    mission = 'PushStonesHeatMapEnv'  # Change according to algorithm
    env_id = mission + '-v0'

    expert_path = '/home/graphics/git/SmartLoader/saved_experts/HeatMap/real_life/lift_23_ep/'

    heat_maps = np.load(expert_path+'heatmap.npy')
    states = np.load(expert_path+'states.npy')
    actions = np.load(expert_path + 'actions.npy')

    heat_map_shape = heat_maps.shape

    hist_size = 1
    heat_map_hist = []

    for kk in range(len(heat_maps)-hist_size):
        heat_map_hist.append( heat_maps[kk:kk+hist_size, :, :])

    heat_map_hist = np.array(heat_map_hist)
    action_hist = np.copy(actions[hist_size:])

    nn_size = [64, 64, 64, 16]
    batch_size = 64
    learning_rate = 5e-4
    epochs = 200




    imitation_learning(heat_map_hist, action_hist, hist_size, nn_size, batch_size, learning_rate, epochs)

if __name__ == '__main__':
    main()