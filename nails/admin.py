from django.contrib import admin, messages

from .models import Nail


@admin.action(description="Reclassify selected nail images")
def reclassify_nail_images(modeladmin, request, queryset):
    """Admin action to reclassify selected nail images"""
    classified_count = 0
    error_count = 0

    for nail in queryset:
        if nail.nail_image:
            try:
                nail.classify_image()
                classified_count += 1
            except Exception as e:
                error_count += 1
                print(f"Error classifying nail {nail.pk}: {e}")

    if classified_count > 0:
        messages.success(
            request, f"Successfully reclassified {classified_count} nail image(s)."
        )
    if error_count > 0:
        messages.error(request, f"Failed to reclassify {error_count} nail image(s).")


@admin.register(Nail)
class NailAdmin(admin.ModelAdmin):
    list_display = ["id", "nail_image", "nail_classification", "confidence_level"]
    list_filter = ["nail_classification"]
    search_fields = ["nail_classification"]
    readonly_fields = [
        "nail_classification",
        "confidence_level",
    ]  # Make classification read-only since it's auto-generated
    actions = [reclassify_nail_images]

    def save_model(self, request, obj, form, change):
        """Override save_model to show classification messages"""
        super().save_model(request, obj, form, change)

        # Show a success message if classification was successful
        if (
            obj.nail_classification
            and obj.nail_classification != "Classification Error"
        ):
            messages.success(
                request,
                f"Image classified as: {obj.nail_classification} with {obj.confidence_level} confidence.",
            )
        elif obj.nail_classification == "Classification Error":
            messages.error(
                request, "Classification failed. Please check the image and try again."
            )
