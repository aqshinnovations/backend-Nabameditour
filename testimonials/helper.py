from .models import Testimonial
from .serializer import TestimonialSerializer


# ================================== Testimonials ====================================


def addTestimonials(request):
    data = request.data

    image = request.FILES.get("image")
    if not image:
        return {
            "code": "400",
            "msg": "Bad request. Please provide a testimonial image.",
        }

    testimonial = Testimonial()
    testimonial.image = image
    testimonial.save()

    return {
        "code": "200",
        "msg": "Testimonial added successfully",
    }


def getTestimonialsList(request):
    testimonials = Testimonial.objects.all()

    serializer = TestimonialSerializer(
        testimonials,
        many=True,
        context={"request": request},
    )

    return {
        "code": "200",
        "list": serializer.data,
    }



def deleteTestimonials(request):
    data = request.GET

    id = data.get("id", None)

    if not id:
        return {
            "code": "400",
            "msg": "Bad request. Please provide testimonial ID.",
        }

    testimonial = Testimonial.objects.filter(id=id).first()

    if not testimonial:
        return {
            "code": "401",
            "msg": "No testimonial found with the provided ID.",
        }

    testimonial.delete()

    return {
        "code": "200",
        "msg": "Testimonial deleted successfully!",
    }