import os.path as osp
import argparse
import torch
import torch.nn.functional as F
from torch_geometric.datasets import Planetoid
import torch_geometric.transforms as T
from torch_geometric.nn import GCNConv, GAE, VGAE
from torch_geometric.utils import train_test_split_edges
from sklearn.linear_model import LogisticRegression
import json
import pickle as pkl


torch.manual_seed(12345)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def load_model(kwargs, args, data, channels):
    """
    定义模型
    """
    class Encoder(torch.nn.Module):
        """
        定义编码器
        两层GCN
        """
        def __init__(self, in_channels, out_channels):
            super(Encoder, self).__init__()
            self.conv1 = GCNConv(in_channels, 2 * out_channels, cached=True)
            if args['model'] in ['GAE']:
                self.conv2 = GCNConv(
                    2 * out_channels, out_channels, cached=True)
            elif args['model'] in ['VGAE']:
                self.conv_mu = GCNConv(
                    2 * out_channels, out_channels, cached=True)
                self.conv_logstd = GCNConv(2 * out_channels, out_channels,
                                            cached=True)
        def forward(self, x, edge_index):
            x = F.relu(self.conv1(x, edge_index))
            if args['model'] in ['GAE']:
                return self.conv2(x, edge_index)
            elif args['model'] in ['VGAE']:
                return self.conv_mu(x, edge_index), self.conv_logstd(x, edge_index)

    model = kwargs[args['model']](
        Encoder(data.num_node_features, channels)).to(device)
    return model


def train(model, optimizer, args, data):
    """
    模型训练
    """
    model.train()
    optimizer.zero_grad()
    z = model.encode(data.x, data.train_pos_edge_index)
    loss = model.recon_loss(z, data.train_pos_edge_index)
    if args['model'] in ['VGAE']:
        loss = loss + (1 / data.num_nodes) * model.kl_loss()
    loss.backward()
    optimizer.step()
    return loss.item()

def main(data):
    """
    主函数入口
    """
    channels = 32 # 设置向量的维度为32
    epoch_num = 100 # 设置迭代次数为100次
    kwargs = {'GAE': GAE, 'VGAE': VGAE}
    args = {'model': 'GAE'}
    data = data.to(device)
    model = load_model(kwargs, args, data, channels)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001) # Adam优化器
    for epoch in range(1, epoch_num+1):
        loss = train(model, optimizer, args, data)
        print(loss)
    return model
    # 得到向量 然后去聚类
    # z = model.encode(data.x, data.train_pos_edge_index)
    # z = z.detach().cpu().numpy()


if __name__ == "__main__":
    """
    原始代码: https://github.com/rusty1s/pytorch_geometric/commit/fb1d3f989688e4ca6989350dc58638f574d98e52
    """
    input_data_path = r'E:\work\gae\data'
    output_path = r'E:\work\gae\data'
    dataset = 'DIP'
    path = osp.join(input_data_path, f'{dataset}_train_datas.pkl')
    train_datas = None
    with open(path, 'rb') as fp:
        train_datas = pkl.load(fp)
        Z = []
        for index, train_data in enumerate(train_datas):
            # 遍历每一幅图
            data = train_data['pg_data']
            model = main(data)
            with torch.no_grad():
                # 得到向量
                z = model.encode(data.x, data.train_pos_edge_index)
                z = z.detach().cpu().numpy()
                Z.append(z)
        # 保存向量
        with open(osp.join(output_path, f'{dataset}_Z.pkl'), 'wb') as wp:
            pkl.dump(Z, wp)



