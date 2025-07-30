

import torch
import torch.nn.functional as F

def compute_iou(preds, targets, threshold=0.5):
    B, _, H, W = preds.shape
    preds = preds.permute(0, 2, 3, 1).reshape(-1, 4)
    targets = targets.permute(0, 2, 3, 1).reshape(-1, 4)

    pred_x1 = preds[:, 0] - preds[:, 2] / 2
    pred_y1 = preds[:, 1] - preds[:, 3] / 2
    pred_x2 = preds[:, 0] + preds[:, 2] / 2
    pred_y2 = preds[:, 1] + preds[:, 3] / 2

    targ_x1 = targets[:, 0] - targets[:, 2] / 2
    targ_y1 = targets[:, 1] - targets[:, 3] / 2
    targ_x2 = targets[:, 0] + targets[:, 2] / 2
    targ_y2 = targets[:, 1] + targets[:, 3] / 2

    inter_x1 = torch.max(pred_x1, targ_x1)
    inter_y1 = torch.max(pred_y1, targ_y1)
    inter_x2 = torch.min(pred_x2, targ_x2)
    inter_y2 = torch.min(pred_y2, targ_y2)

    inter_area = (inter_x2 - inter_x1).clamp(0) * (inter_y2 - inter_y1).clamp(0)
    pred_area = (pred_x2 - pred_x1).clamp(0) * (pred_y2 - pred_y1).clamp(0)
    targ_area = (targ_x2 - targ_x1).clamp(0) * (targ_y2 - targ_y1).clamp(0)

    union_area = pred_area + targ_area - inter_area + 1e-6
    iou = inter_area / union_area
    return (iou > threshold).float().mean().item()

def train_detection(model, train_dl, val_dl=None, epochs=20, lr=1e-3, device="cuda", save_checkpoint=True, manual_seed=69):
    '''
    train_dl and val_dl should both return the following format: (img, target). They should be tensors.
    '''
    model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    torch.manual_seed(manual_seed)
    torch.cuda.manual_seed_all(manual_seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

    for epoch in range(epochs):
        model.train()
        total_loss = 0.0
        total_iou = 0.0
        count = 0
        for imgs, targets in train_dl:
            imgs = imgs.to(device)
            targets = targets.to(device)

            preds = model(imgs)
            bbox_preds = preds[:, :4, :, :]
            obj_preds = preds[:, 4:, :, :]
            bbox_targets = targets[:, :4, :, :]
            obj_targets = targets[:, 4:, :, :]

            bbox_loss = F.mse_loss(bbox_preds, bbox_targets)
            obj_loss = F.binary_cross_entropy_with_logits(obj_preds, obj_targets)
            loss = bbox_loss + obj_loss

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            total_iou += compute_iou(bbox_preds, bbox_targets)
            count += 1
            print(f"Epoch [{epoch+1:02d}/{epochs:02d}] | Train Loss: {total_loss/count:.4f} | Train IoU: {total_iou/count:.4f}", end='\r')

        print()
        avg_train_loss = total_loss / len(train_dl)
        avg_train_iou = total_iou / len(train_dl)

        if val_dl is not None:
            model.eval()
            val_loss = 0.0
            val_iou = 0.0
            val_count = 0
            with torch.inference_mode():
                for imgs, targets in val_dl:
                    imgs = imgs.to(device)
                    targets = targets.to(device)

                    preds = model(imgs)
                    bbox_preds = preds[:, :4, :, :]
                    obj_preds = preds[:, 4:, :, :]
                    bbox_targets = targets[:, :4, :, :]
                    obj_targets = targets[:, 4:, :, :]

                    bbox_loss = F.mse_loss(bbox_preds, bbox_targets)
                    obj_loss = F.binary_cross_entropy_with_logits(obj_preds, obj_targets)
                    loss = bbox_loss + obj_loss

                    val_loss += loss.item()
                    val_iou += compute_iou(bbox_preds, bbox_targets)
                    val_count += 1
                    print(f"Epoch [{epoch+1:02d}/{epochs:02d}] | Val   Loss: {val_loss/val_count:.4f} | Val   IoU: {val_iou/val_count:.4f}", end='\r')

            print()
            avg_val_loss = val_loss / len(val_dl)
            avg_val_iou = val_iou / len(val_dl)
            print(f"Epoch [{epoch+1:02d}/{epochs:02d}] | Train Loss: {avg_train_loss:.4f} | Train IoU: {avg_train_iou:.4f} || Val Loss: {avg_val_loss:.4f} | Val IoU: {avg_val_iou:.4f}")
        else:
            print(f"Epoch [{epoch+1:02d}/{epochs:02d}] | Train Loss: {avg_train_loss:.4f} | Train IoU: {avg_train_iou:.4f}")

        if save_checkpoint:
            torch.save(model.state_dict(), f"DetectionWeights_epoch{epoch+1}.pth")

    return model

def train_recognition(model, train_dl, val_dl=None, epochs=20, lr=1e-3, device="cuda", save_checkpoint=True, manual_seed=69):
    '''
    train_dl and val_dl should both return the following format: (img, target). They should be tensors.
    '''
    model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = torch.nn.CrossEntropyLoss()

    torch.manual_seed(manual_seed)
    torch.cuda.manual_seed_all(manual_seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

    for epoch in range(epochs):
        model.train()
        total_loss = 0.0
        total_correct = 0
        total_samples = 0
        for imgs, labels in train_dl:
            imgs = imgs.to(device)
            labels = labels.to(device)

            logits = model(imgs, labels)
            loss = criterion(logits, labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            preds = logits.argmax(dim=1)
            total_correct += (preds == labels).sum().item()
            total_samples += labels.size(0)

            print(f"Epoch [{epoch+1:02d}/{epochs:02d}] | Train Loss: {total_loss/(total_samples):.4f} | Train Acc: {100 * total_correct / total_samples:6.2f}%", end='\r')

        print()
        avg_train_loss = total_loss / len(train_dl)
        train_acc = total_correct / total_samples * 100

        if val_dl is not None:
            model.eval()
            val_loss = 0.0
            val_correct = 0
            val_samples = 0
            val_count = 0
            with torch.inference_mode():
                for imgs, labels in val_dl:
                    imgs = imgs.to(device)
                    labels = labels.to(device)

                    logits = model(imgs, labels)
                    loss = criterion(logits, labels)

                    val_loss += loss.item()
                    preds = logits.argmax(dim=1)
                    val_correct += (preds == labels).sum().item()
                    val_samples += labels.size(0)
                    val_count += 1
                    print(f"Epoch [{epoch+1:02d}/{epochs:02d}] | Val   Loss: {val_loss/val_count:.4f} | Val   Acc: {100 * val_correct / val_samples:6.2f}%", end='\r')

            print()
            avg_val_loss = val_loss / len(val_dl)
            avg_val_acc = val_correct / val_samples * 100
            print(f"Epoch [{epoch+1:02d}/{epochs:02d}] | Train Loss: {avg_train_loss:.4f} | Train Acc: {train_acc:.2f}% || Val Loss: {avg_val_loss:.4f} | Val Acc: {avg_val_acc:.2f}%")
        else:
            print(f"Epoch [{epoch+1:02d}/{epochs:02d}] | Train Loss: {avg_train_loss:.4f} | Train Acc: {train_acc:.2f}%")

        if save_checkpoint:
            torch.save(model.state_dict(), f"RecognitionWeights_epoch{epoch+1}.pth")

    return model














