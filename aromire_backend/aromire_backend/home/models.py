import logging
import requests

from django.conf import settings
from django.db import models
from django.shortcuts import redirect
from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel, FieldRowPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from modelcluster.fields import ParentalKey
from cloudinary_storage.storage import VideoMediaCloudinaryStorage


logger = logging.getLogger(__name__)


# ── Must be defined before HomePage ───────────────────────────────────────────

class HomePillar(Orderable):
    page        = ParentalKey('home.HomePage', on_delete=models.CASCADE, related_name='pillars')
    icon        = models.CharField(max_length=10, default="🌱", help_text="Paste an emoji")
    heading     = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    panels = [
        FieldPanel('icon'),
        FieldPanel('heading'),
        FieldPanel('description'),
    ]

    class Meta:
        verbose_name = "Pillar"


class ProgramMedia(Orderable):
    page    = ParentalKey('home.GalleryProgramPage', on_delete=models.CASCADE, related_name='media')
    image   = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    video   = models.FileField(
        upload_to='gallery/videos/',
        null=True,
        blank=True,
        storage=VideoMediaCloudinaryStorage(),
    )
    caption = models.CharField(max_length=200, blank=True)

    panels = [
        FieldPanel('image'),
        FieldPanel('video'),
        FieldPanel('caption'),
    ]

    class Meta:
        verbose_name = "Media"


class ContactFormField(AbstractFormField):
    page = ParentalKey('home.ContactPage', on_delete=models.CASCADE, related_name='form_fields')


# ── Page models ───────────────────────────────────────────────────────────────

class GalleryProgramPage(Page):
    description = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        InlinePanel('media', label="Photos & Videos"),
    ]

    parent_page_types = ['home.GalleryPage']
    subpage_types = []

    class Meta:
        verbose_name = "Gallery Program"


class HomePage(Page):
    hero_eyebrow  = models.CharField(max_length=100, default="Empowering Communities, Transforming Lives")
    hero_title    = models.CharField(max_length=200, default="Building a Stronger Community Together")
    hero_subtitle = models.TextField(blank=True)
    hero_logo     = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_eyebrow'),
            FieldPanel('hero_title'),
            FieldPanel('hero_subtitle'),
            FieldPanel('hero_logo'),
        ], heading="Hero Section"),
        InlinePanel('pillars', label="Pillars"),
    ]

    parent_page_types = ['wagtailcore.Page']
    subpage_types = ['home.AboutPage', 'home.GalleryPage', 'home.ContactPage']

    def get_context(self, request):
        context = super().get_context(request)
        carousel_images = []
        for program in GalleryProgramPage.objects.live():
            for item in program.media.all():
                if item.image:
                    carousel_images.append(item)
        context['carousel_images'] = carousel_images
        return context

    class Meta:
        verbose_name = "Home Page"


class AboutPage(Page):
    eyebrow  = models.CharField(max_length=100, default="Who We Are")
    heading  = models.CharField(max_length=200, default="Rooted in Purpose, Driven by People")
    intro    = models.TextField(blank=True)
    image    = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    mission  = models.TextField(blank=True)
    vision   = models.TextField(blank=True)
    values   = models.TextField(blank=True)
    approach = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('eyebrow'),
            FieldPanel('heading'),
            FieldPanel('intro'),
            FieldPanel('image'),
        ], heading="About Section"),
        MultiFieldPanel([
            FieldPanel('mission'),
            FieldPanel('vision'),
            FieldPanel('values'),
            FieldPanel('approach'),
        ], heading="Our Values"),
    ]

    parent_page_types = ['home.HomePage']
    subpage_types = []

    class Meta:
        verbose_name = "About Page"


class GalleryPage(Page):
    eyebrow = models.CharField(max_length=100, default="Our Moments")
    heading = models.CharField(max_length=200, default="Gallery")
    intro   = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('eyebrow'),
            FieldPanel('heading'),
            FieldPanel('intro'),
        ], heading="Gallery Header"),
    ]

    parent_page_types = ['home.HomePage']
    subpage_types = ['home.GalleryProgramPage']

    def get_context(self, request):
        context = super().get_context(request)
        context['programs'] = self.get_children().live().specific()
        return context

    class Meta:
        verbose_name = "Gallery Page"


class ContactPage(AbstractEmailForm):
    eyebrow = models.CharField(max_length=100, default="Reach Out")
    heading = models.CharField(max_length=200, default="Let's Build Together")
    intro   = models.TextField(blank=True)

    thank_you_text = models.TextField(
        blank=True,
        default="Thank you for reaching out. We will get back to you soon."
    )

    brevo_list_id = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Optional Brevo list ID. Leave blank to use BREVO_DEFAULT_LIST_ID from settings."
    )

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        MultiFieldPanel([
            FieldPanel('eyebrow'),
            FieldPanel('heading'),
            FieldPanel('intro'),
        ], heading="Contact Header"),
        InlinePanel('form_fields', label="Contact Form Fields"),
        FieldPanel('thank_you_text'),
        FieldPanel('brevo_list_id'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], heading="Email Notification Settings"),
    ]

    parent_page_types = ['home.HomePage']
    subpage_types = []

    def get_context(self, request):
        context = super().get_context(request)
        context['form_sent'] = request.GET.get('sent') == '1'
        return context

    def render_landing_page(self, request, form_submission=None, *args, **kwargs):
        return redirect(self.get_url(request) + '?sent=1')

    def process_form_submission(self, form):
        submission = super().process_form_submission(form)
        try:
            self.send_contact_to_brevo(form.cleaned_data)
        except Exception:
            logger.exception("Brevo contact sync failed")
        return submission

    def send_contact_to_brevo(self, cleaned_data):
        api_key = getattr(settings, 'BREVO_API_KEY', None)
        if not api_key:
            logger.warning("BREVO_API_KEY is not set")
            return

        email = (
            cleaned_data.get('email')
            or cleaned_data.get('email_address')
            or cleaned_data.get('email_address_')
        )
        if not email:
            logger.warning("No email field found in Wagtail form submission")
            return

        first_name = cleaned_data.get('first_name', '')
        last_name  = cleaned_data.get('last_name', '')
        phone      = cleaned_data.get('phone', '')
        message    = cleaned_data.get('message', '')
        interest   = (
            cleaned_data.get('interest')
            or cleaned_data.get('im_interested_in')
            or cleaned_data.get('i_m_interested_in')
            or ''
        )

        list_id = self.brevo_list_id or getattr(settings, 'BREVO_DEFAULT_LIST_ID', None)

        payload = {
            'email': email,
            'attributes': {
                'FNAME':    str(first_name),
                'LNAME':    str(last_name),
                'INTEREST': str(interest),
                'MESSAGE':  str(message),
            },
            'updateEnabled': True,
        }
        if phone:
            payload['attributes']['SMS'] = str(phone)
        if list_id:
            payload['listIds'] = [int(list_id)]

        headers = {
            'api-key':      api_key,
            'Content-Type': 'application/json',
            'Accept':       'application/json',
        }

        response = requests.post(
            'https://api.brevo.com/v3/contacts',
            json=payload,
            headers=headers,
            timeout=10,
        )
        response.raise_for_status()

    class Meta:
        verbose_name = "Contact Page"