# 🧰 Toolbox Project - Files handling

![Toolbox Badge](https://img.shields.io/badge/Toolbox-Files%20handling-purple?style=flat-square&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.x-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

This app is part of the **Toolbox Project**, a collection of modular, production-grade Django utilities. This specific module focuses on robust, clean, and scalable **image file management**.

---

## ✨ Key Features

### 📁 Intelligent File Lifecycle Management
- ✅ When a record is deleted, the **related image is automatically removed** from the file system.
- 🔄 Replace images dynamically using a **custom file widget** (`customFileInput`) with a clear and intuitive UX.
- ♲ Safely remove replaced images to keep storage clean.

### 📸 Multi-Image Upload Support
- 📎 Upload up to **3 images simultaneously** using a single `ImageField` input.
- 📂 Each image is:
  - Stored in the **same folder**, defined per model instance
  - Folder name is saved in the model (timestamp-based)
  - File names use **UUIDs** to ensure uniqueness

### ⚙️ Image Management Logic
- ✅ Modify or delete child images from the same form.
- ⚡ A dynamic helper `checkFilesReplace()` handles whether an image should be:
  - ❌ Deleted
  - 🔄 Replaced
  - ✉️ Left unchanged

### 🔮 Custom Validators
All uploaded files are validated against:
- ✅ Allowed file extensions
- ✅ Maximum file size (per image)
- ✅ Total combined size (for multi-image uploads)

---

## ⚙️ Project Configuration

Add the following settings to your `settings.py` to configure global validation behavior:

```python
# 📦 CUSTOM FILE CONFIGURATION
CUSTOM_FILE_EXTENSIONS = ['jpeg', 'jpg', 'png']
MAXINUM_MULTI_FILE = 3
TOTAL_FILE_SIZE = 200         # KB (per file)
TOTAL_MULTI_FILE_SIZE = 600   # KB (total combined)
```

These values are used by custom validators in forms and models to strictly enforce upload policies.

---

## 🧰 Widget: `customFileInput`

The custom widget:
- Displays the current image as a preview 🖼️
- Includes a checkbox labeled `Remove` to clear the current image ❌
- Designed as a drop-in replacement for Django's `ClearableFileInput`
- Bootstrap-compatible and fully customizable via template override

---

## ✔️ Best Practices Implemented

| Practice                     | Description                                       |
|-----------------------------|---------------------------------------------------|
| DRY                         | Reusable logic via utilities and widget templates |
| File safety                 | UUID naming + physical deletion of removed images |
| Scoped media folders        | Timestamp + model-defined directories             |
| Custom field validation     | Clean and strict validation with clear feedback   |
| Template-based widget logic | Great UX and maintainability                      |

---

## 🔍 Example Usage

```python
class SampleRecordModelForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        widget=ClearableFileInput(attrs={'class': 'form-control'}),
        validators=[
            FileExtensionValidator(
                allowed_extensions=settings.CUSTOM_FILE_EXTENSIONS,
                message="Invalid file extension"
            ),
            imagesTotalSize_validator,
        ]
    )

    class Meta:
        model = SampleRecord
        fields = ['title', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.template_name = 'widgets/customFileInput.html'
```

---

## 📂 Folder Strategy

Uploaded images are saved under:

```
media/<app_name>/<timestamp>/
```

Each image filename is UUID-based:

```
8f42de8912d44fdb9d6c71a923c9a5b2.jpg
```

This prevents name collisions and simplifies cleanup.

---

## 📺 Future Improvements

- 🚀 Drag-and-drop UI for uploads
- 📊 Upload progress tracking
- 🧼 Background job for orphaned file cleanup

---

## 🤝 Credits

Thanks for following the development of Toolbox project on GitHub. Contributions and feedback are welcome to continue improving and scaling the platform.

---

> Built with Django ❤️
