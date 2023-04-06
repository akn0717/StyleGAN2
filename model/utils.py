import pickle
import os

from model.configs import *
def save_models(save_path, G, D, optimizer_G, optimizer_D, visual_z):
    print("Saving...",end='')
    if not(os.path.exists(save_path)):
        os.makedirs(save_path)

    with open(save_path + "/Generator.pkl", "wb") as f:
        G_pkl = {
            "model": G,
            "optimizer": optimizer_G
        }
        pickle.dump(G_pkl, f)

    with open(save_path + "/Discriminator.pkl", "wb") as f:
        D_pkl = {
            "model": D,
            "optimizer": optimizer_D
        }
        pickle.dump(D_pkl, f)

    with open(save_path + "/static_noise_seed.pkl", "wb") as f:
        static_noise_seed_pkl = {
            "visual_z": visual_z,
        }
        pickle.dump(static_noise_seed_pkl, f)
        
    print("Done!")


def load_models(model_file_path):
    print("Loading pretrained models...", end = '')
    G = optimizer_G = D = optimizer_D = visual_z = None
    with open(model_file_path + "/Generator.pkl", "rb") as f:
        G_pkl = pickle.load(f)
        G = G_pkl["model"]
        optimizer_G = G_pkl["optimizer"]

    with open(model_file_path + "/Discriminator.pkl", "rb") as f:
        D_pkl = pickle.load(f)
        D = D_pkl["model"]
        optimizer_D = D_pkl["optimizer"]

    with open(model_file_path + "/static_noise_seed.pkl", "rb") as f:
        static_noise_seed_pkl = pickle.load(f)
        visual_z = static_noise_seed_pkl["visual_z"]
    print("Done!")
    return G, optimizer_G, D, optimizer_D, visual_z

def sampling_large_batch(G, batch_size, minibatch_size, device):
    out_samples = None
    while (batch_size > 0):
        minibatch_size = min(minibatch_size, batch_size)
        with torch.no_grad():
            z = torch.randn(minibatch_size, LATENT_SIZE).to(device)
            samples = G(z.to(DEVICE)).to(device)
        if out_samples is None:
            out_samples = samples
        else:
            out_samples = torch.cat((out_samples, samples))
        
        batch_size -= minibatch_size
    return out_samples