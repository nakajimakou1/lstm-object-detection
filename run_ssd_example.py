from vision.ssd.vgg_ssd import create_vgg_ssd, create_vgg_ssd_predictor
from vision.ssd.mobilenetv1_ssd import create_mobilenetv1_ssd, create_mobilenetv1_ssd_predictor
from vision.ssd.mobilenetv1_ssd_lite import create_mobilenetv1_ssd_lite, create_mobilenetv1_ssd_lite_predictor
from vision.ssd.squeezenet_ssd_lite import create_squeezenet_ssd_lite, create_squeezenet_ssd_lite_predictor
from vision.ssd.mobilenet_v2_ssd_lite import create_mobilenetv2_ssd_lite, create_mobilenetv2_ssd_lite_predictor
from vision.ssd.resnet50_ssd1 import create_resnet18_ssd, create_resnet18_ssd_predictor
from vision.utils.misc import Timer
import cv2
import sys
import numpy as np


if len(sys.argv) < 5:
    print('Usage: python run_ssd_example.py <net type>  <model path> <label path> <image path>')
    sys.exit(0)
net_type = sys.argv[1]
model_path = sys.argv[2]
label_path = sys.argv[3]
image_path = sys.argv[4]

class_names = [name.strip() for name in open(label_path).readlines()]


if net_type == 'vgg16-ssd':
    net = create_vgg_ssd(len(class_names), is_test=True)
elif net_type == 'mb1-ssd':
    net = create_mobilenetv1_ssd(len(class_names), is_test=True)
elif net_type == 'mb1-ssd-lite':
    net = create_mobilenetv1_ssd_lite(len(class_names), is_test=True)
elif net_type == 'mb2-ssd-lite':
    net = create_mobilenetv2_ssd_lite(len(class_names), is_test=True)
elif net_type == 'sq-ssd-lite':
    net = create_squeezenet_ssd_lite(len(class_names), is_test=True)
elif net_type == 'resnet-18':
    net = create_resnet18_ssd(len(class_names), is_test=True)
else:
    print("The net type is wrong. It should be one of vgg16-ssd, mb1-ssd and mb1-ssd-lite.")
    sys.exit(1)
net.load(model_path)

if net_type == 'vgg16-ssd':
    predictor = create_vgg_ssd_predictor(net, candidate_size=200)
elif net_type == 'mb1-ssd':
    predictor = create_mobilenetv1_ssd_predictor(net, candidate_size=200)
elif net_type == 'mb1-ssd-lite':
    predictor = create_mobilenetv1_ssd_lite_predictor(net, candidate_size=200)
elif net_type == 'mb2-ssd-lite':
    predictor = create_mobilenetv2_ssd_lite_predictor(net, candidate_size=200)
elif net_type == 'sq-ssd-lite':
    predictor = create_squeezenet_ssd_lite_predictor(net, candidate_size=200)
elif net_type == 'resnet-18':
    predictor = create_resnet18_ssd_predictor(net, candidate_size=200)
else:
    predictor = create_vgg_ssd_predictor(net, candidate_size=200)

orig_image = cv2.imread(image_path)
img1 = cv2.imread('/Users/pranoyr/PycharmProjects/Pytorch/lstm-object-detection-new/data/JPEGImages/000005.jpg')
img2 = cv2.imread('/Users/pranoyr/PycharmProjects/Pytorch/lstm-object-detection-new/data/JPEGImages/000007.jpg')
img3 = cv2.imread('/Users/pranoyr/PycharmProjects/Pytorch/lstm-object-detection-new/data/JPEGImages/000009.jpg')
img4 = cv2.imread('/Users/pranoyr/PycharmProjects/Pytorch/lstm-object-detection-new/data/JPEGImages/000012.jpg')
img5 = cv2.imread('/Users/pranoyr/PycharmProjects/Pytorch/lstm-object-detection-new/data/JPEGImages/000016.jpg')

video = [img1,img2,img3,img4,img5]


hidden_states_list = [None for i in range(6)]
for image in video:
    hidden_states_list, boxes, labels, probs = predictor.predict(image, hidden_states_list, 10, 0.4)

print(boxes.shape)


for i in range(boxes.size(0)):
    box = boxes[i, :]
    cv2.rectangle(img5, (box[0], box[1]), (box[2], box[3]), (255, 255, 0), 4)
    #label = f"""{voc_dataset.class_names[labels[i]]}: {probs[i]:.2f}"""
    label = f"{class_names[labels[i]]}: {probs[i]:.2f}"
    cv2.putText(img5, label,
                (box[0] + 20, box[1] + 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,  # font scale
                (255, 0, 255),
                2)  # line type
path = "run_ssd_example_output.jpg"
cv2.imwrite(path, img5)
print(f"Found {len(probs)} objects. The output image is {path}")
