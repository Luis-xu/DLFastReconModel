"""This is the basic unet model"""
import sys
import os
import torch
import torch.nn as nn
from UnetParts import *

class Unet(nn.Module):
    def __init__(self, n_channels_in, n_channels_out, bilinear = True, ispooling = True):
        super(Unet, self).__init__()

        self.n_channels_in = n_channels_in
        self.n_channels_out = n_channels_out
        self.bilinear = bilinear
        self.ispooling = ispooling

        self.inconv = DoubleConv(n_channels_in, 32)
        self.down1 = Down(32, 64, self.ispooling)
        self.down2 = Down(64, 128, self.ispooling)
        self.down3 = Down(128, 256, self.ispooling)
        if self.bilinear:
            factor = 2
        else:
            factor = 1
        self.down4 = Down(256, 512//factor, self.ispooling)
        self.up1 = UP(512, 256//factor, self.bilinear)
        self.up2 = UP(256, 128//factor, self.bilinear)
        self.up3 = UP(128, 64//factor, self.bilinear)
        self.up4 = UP(64, 32, self.bilinear)
        self.outconv = OutConv(32, n_channels_out)
        self.drop = nn.Dropout2d(p=0.4)
    def forward(self, x):
        x1 = self.inconv(x)
        x2 = self.down1(x1)
        x3 = self.down2(x2)
        x4 = self.down3(x3)
        x5 = self.down4(x4)
        x = self.up1(x5, x4)
        x = self.up2(x, x3)
        x = self.up3(x, x2)
        x = self.up4(x, x1)
        x = self.drop(x)
        out = self.outconv(x)
        out = torch.clamp(out,0,1)
        return out,x



# tensor = torch.rand(4,1,256,256)
# model = Unet(1, 1)
# resutl = model(tensor)

