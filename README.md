# Foundation Model for Remote Sensing Multispectral Image
This project aims to study and implement foundation model for Remote Sensing Multispectral Image.
- Using Masked Image Modeling (MIM) approach with [SimMIM](https://arxiv.org/abs/2111.09886).
- Using [Swin Transformer](https://arxiv.org/abs/2103.14030) as the backbone model because hierarchical design can be beneficial for remote sensing data.
- Using Sentinel-2A from [SSL4EO-S12](https://github.com/zhu-xlab/SSL4EO-S12) with removing 3 spectral bands from 13 bands. The following bands are considered.
  - B2 Blue
  - B3 Green
  - B4 Red
  - B5 Vegetation Red Edge
  - B6 Vegetation Red Edge
  - B7 Vegetation Red Edge
  - B8 NIR
  - B8A NIR
  - B11 SWIR
  - B12 SWIR
- Aim to experiment masked patch size and masking ratio.
  
## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

This project uses code from the following MIT-licensed project:
- Swin Transformer by microsoft - [GitHub Repository](https://github.com/microsoft/Swin-Transformer)
- SimMIM by microsoft - [GitHub Repository](https://github.com/microsoft/SimMIM)
