import cv2
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.conf import settings
from .models import Image
from cellpose import models, io
from django.conf.urls.static import static
from os import path
from typing import List
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import FileSystemStorage





def process_image(request):
    if request.method != 'POST' or not request.FILES.getlist('image'):
        return HttpResponse('ERROR!!!')
    
    image_list: List[InMemoryUploadedFile] = request.FILES.getlist('image')
    fs = FileSystemStorage()

    filenames = [path.join(settings.MEDIA_ROOT, fs.save(i.name, i)) for i in image_list]
    images = [io.imread(f) for f in filenames]

    model = models.Cellpose(gpu=False, model_type=request.POST['model'])
    diameter = 0; flow_threshold = 0.4; cellprob_threshold = 0.0

    files = [path.join(settings.MEDIA_ROOT, path.splitext(f)[0]) for f in filenames]
    print(files)

    # run model on test images
    out = model.eval(images,
                                  diameter=diameter,
                                  flow_threshold=flow_threshold,
                                  cellprob_threshold=cellprob_threshold
                                  )
    
    io.save_masks(images, 
              out[0], 
              out[1], 
              files, 
              png=True, # save masks as PNGs and save example image
              tif=True, # save masks as TIFFs
              save_txt=True, # save txt outlines for ImageJ
              save_flows=False, # save flows as TIFFs
              save_outlines=False, # save outlines as TIFFs 
              )
    
    for file in files:
        fixed_file_name = path.basename(file + "_cp_output.png")
        image = Image(filename=fixed_file_name, width=3600, height=900)
        image.save()
    
    return HttpResponse('Bild erfolgreich verarbeitet.')

def index(request):
    return render(request, 'processing/index.html', {
        "models": models.MODEL_NAMES
    })

def image_list(request):
    images = Image.objects.all()
    return render(request, 'processing/image_list.html', {'images': images})


def delete_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    if request.method == 'POST':
        image.delete()
        return redirect('image_list')