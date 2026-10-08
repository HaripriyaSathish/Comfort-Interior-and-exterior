from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify


# ------------------------------------------------------------------
# BASE CLASSES
# ------------------------------------------------------------------
class SingletonModel(models.Model):
    """A model that can only ever have one row (pk=1)."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # never delete the single settings row

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class OrderedModel(models.Model):
    display_order = models.PositiveIntegerField(
        'Display order', default=0,
        help_text='Lower numbers appear first.',
    )
    is_active = models.BooleanField('Show on website', default=True)

    class Meta:
        abstract = True
        ordering = ['display_order', 'id']


# ------------------------------------------------------------------
# SITE SETTINGS (logo, favicon, brand name)
# ------------------------------------------------------------------
class SiteSettings(SingletonModel):
    site_name = models.CharField(
        'Company name', max_length=150,
        default='Classic Comfort Interior and Exterior',
    )
    logo = models.ImageField(
        'Logo', upload_to='site/', blank=True, null=True,
        help_text='Shown in the navbar and also used as the browser tab icon (favicon). '
                  'A square image works best.',
    )
    nav_button_text = models.CharField(
        'Navbar button text', max_length=50, default='Get a Quote',
        help_text='The button on the right of the navbar. It scrolls to the Contact section.',
    )

    # --- SEO (Google search results) ---
    meta_title = models.CharField(
        'Page title', max_length=100,
        default='Classic Comfort Interior and Exterior | Interior, Exterior & Commercial Design',
        help_text='Shown in the browser tab and as the blue link in Google. Keep under 60–70 characters.',
    )
    meta_description = models.TextField(
        'Meta description', max_length=170,
        default='From bespoke kitchens and wardrobes to striking facades and commercial fit-outs, '
                'Classic Comfort designs and builds every detail, end to end.',
        help_text='The short summary under the link in Google. Keep under 155–160 characters.',
    )
    meta_keywords = models.CharField(
        'Keywords', max_length=255, blank=True,
        default='interior design, exterior design, commercial interiors, modular kitchen, '
                'wardrobes, facade design, home renovation',
        help_text='Comma separated words people might search for.',
    )
    meta_author = models.CharField('Author', max_length=100, blank=True,
                                   default='Classic Comfort Interior and Exterior')
    canonical_url = models.URLField(
        'Website address', blank=True,
        help_text='Full live address of the website, e.g. https://www.classiccomfort.in',
    )
    allow_search_engines = models.BooleanField(
        'Allow Google to show this website', default=True,
        help_text='Untick only while the site is under construction.',
    )

    # --- Social sharing (WhatsApp, Facebook, LinkedIn previews) ---
    og_title = models.CharField(
        'Share title', max_length=100, blank=True,
        help_text='Title shown when the link is shared. Leave blank to use the page title.',
    )
    og_description = models.CharField(
        'Share description', max_length=200, blank=True,
        help_text='Leave blank to use the meta description.',
    )
    og_image = models.ImageField(
        'Share image', upload_to='site/', blank=True, null=True,
        help_text='Preview image when the link is shared. 1200 × 630 px recommended. '
                  'Leave blank to use the hero background.',
    )

    # --- Tracking / verification ---
    google_site_verification = models.CharField(
        'Google Search Console code', max_length=100, blank=True,
        help_text='Only the content value from the google-site-verification meta tag.',
    )
    google_analytics_id = models.CharField(
        'Google Analytics ID', max_length=30, blank=True,
        help_text='e.g. G-XXXXXXXXXX',
    )

    class Meta:
        verbose_name = 'Website Settings'
        verbose_name_plural = 'Website Settings'

    def __str__(self):
        return 'Website Settings'

    @property
    def share_title(self):
        return self.og_title or self.meta_title

    @property
    def share_description(self):
        return self.og_description or self.meta_description


# ------------------------------------------------------------------
# NAVBAR MENU
# ------------------------------------------------------------------
class NavMenuItem(OrderedModel):
    SECTION_CHOICES = [
        ('home', 'Home (top of page)'),
        ('about', 'About section'),
        ('interior', 'Interior section'),
        ('exterior', 'Exterior section'),
        ('projects', 'Projects section'),
        ('contact', 'Contact section'),
    ]

    label = models.CharField('Menu text', max_length=50)
    section = models.CharField(
        'Scrolls to', max_length=30, choices=SECTION_CHOICES,
        help_text='Which part of the page this link scrolls to.',
    )

    class Meta(OrderedModel.Meta):
        verbose_name = 'Navbar Menu Link'
        verbose_name_plural = 'Navbar Menu Links'

    def __str__(self):
        return self.label

    @property
    def anchor(self):
        return f'#{self.section}'


# ------------------------------------------------------------------
# HERO SECTION
# ------------------------------------------------------------------
class HeroSection(SingletonModel):
    tagline = models.CharField(
        'Small text above heading', max_length=150,
        default='Interior • Exterior • Commercial',
    )
    heading = models.CharField(
        'Main heading', max_length=200,
        default='Crafting Spaces That Feel Like Home',
    )
    description = models.TextField(
        'Description',
        default='From bespoke kitchens and wardrobes to striking facades and commercial '
                'fit-outs — we design and build every detail, end to end.',
    )
    background_image = models.ImageField(
        'Background image', upload_to='hero/', blank=True, null=True,
        help_text='Large landscape photo (at least 1920px wide recommended).',
    )
    primary_button_text = models.CharField(
        'Main button text', max_length=50, default='Explore Our Work',
        help_text='Scrolls down to the Interior section.',
    )
    secondary_button_text = models.CharField(
        'Second button text', max_length=50, default='Get a Quote',
        help_text='Scrolls down to the Contact section.',
    )

    class Meta:
        verbose_name = 'Hero Banner (Top Section)'
        verbose_name_plural = 'Hero Banner (Top Section)'

    def __str__(self):
        return 'Hero Banner'


# ------------------------------------------------------------------
# ABOUT US SECTION
# ------------------------------------------------------------------
HIGHLIGHT_HELP = ('Wrap words in *stars* to show them in gold, or in _underscores_ for italic. '
                  'Leave an empty line between paragraphs.')


class AboutSection(SingletonModel):
    section_label = models.CharField('Small heading', max_length=50, default='About Us')
    intro = models.CharField('Opening line', max_length=255, blank=True, help_text=HIGHLIGHT_HELP)
    content = models.TextField('Main text', blank=True, help_text=HIGHLIGHT_HELP)
    closing_text = models.TextField('Closing lines', blank=True, help_text=HIGHLIGHT_HELP)
    image = models.ImageField(
        'Side image', upload_to='about/', blank=True, null=True,
        help_text='Tall portrait photo works best (about 3:4).',
    )

    vision_title = models.CharField('Vision heading', max_length=100, default='Our Vision')
    vision_text = models.CharField('Vision text', max_length=255, blank=True, help_text=HIGHLIGHT_HELP)

    promise_title = models.CharField('Promise heading', max_length=100, default='Our Promise')

    class Meta:
        verbose_name = 'About Us Section'
        verbose_name_plural = 'About Us Section'

    def __str__(self):
        return 'About Us Section'


class AboutWorkType(OrderedModel):
    """The 'Interior / Exterior / Commercial — WORKS' row under the vision."""
    about = models.ForeignKey(AboutSection, on_delete=models.CASCADE, related_name='work_types', default=1)
    title = models.CharField('Title', max_length=50)
    subtitle = models.CharField('Small text below', max_length=50, default='Works')
    section = models.CharField(
        'Scrolls to', max_length=30, choices=NavMenuItem.SECTION_CHOICES, blank=True,
        help_text='Optional: clicking it scrolls to this section.',
    )

    class Meta(OrderedModel.Meta):
        verbose_name = 'Work type'
        verbose_name_plural = 'Work types (Interior / Exterior / Commercial row)'

    def __str__(self):
        return self.title


class AboutPromise(OrderedModel):
    """Words in the 'Our Promise' line, joined with • on the website."""
    about = models.ForeignKey(AboutSection, on_delete=models.CASCADE, related_name='promises', default=1)
    text = models.CharField('Promise', max_length=60)

    class Meta(OrderedModel.Meta):
        verbose_name = 'Promise'
        verbose_name_plural = 'Our Promise words'

    def __str__(self):
        return self.text


# ------------------------------------------------------------------
# SERVICE SECTIONS (Interior Works, and later Exterior Works)
# ------------------------------------------------------------------
class BaseServiceSection(SingletonModel):
    section_label = models.CharField('Small heading', max_length=60)
    heading = models.CharField('Main heading', max_length=100)
    description = models.CharField('Description', max_length=255, blank=True)
    enquire_button_text = models.CharField(
        'Card button text', max_length=30, default='Enquire',
        help_text='Shown on every card. Clicking it scrolls to the Contact section.',
    )

    class Meta:
        abstract = True


class BaseServiceItem(OrderedModel):
    title = models.CharField('Title', max_length=80)
    description = models.CharField('Short description', max_length=200)
    image = models.ImageField('Image', upload_to='services/', blank=True, null=True,
                              help_text='Landscape photo (about 4:3).')

    class Meta(OrderedModel.Meta):
        abstract = True

    def __str__(self):
        return self.title


class InteriorSection(BaseServiceSection):
    class Meta:
        verbose_name = 'Interior Works Section'
        verbose_name_plural = 'Interior Works Section'

    def __str__(self):
        return 'Interior Works Section'


class InteriorService(BaseServiceItem):
    section = models.ForeignKey(InteriorSection, on_delete=models.CASCADE,
                                related_name='services', default=1)

    class Meta(BaseServiceItem.Meta):
        verbose_name = 'Interior service card'
        verbose_name_plural = 'Interior service cards'


class ExteriorSection(BaseServiceSection):
    class Meta:
        verbose_name = 'Exterior & Commercial Works Section'
        verbose_name_plural = 'Exterior & Commercial Works Section'

    def __str__(self):
        return 'Exterior & Commercial Works Section'


class ExteriorService(BaseServiceItem):
    section = models.ForeignKey(ExteriorSection, on_delete=models.CASCADE,
                                related_name='services', default=1)

    class Meta(BaseServiceItem.Meta):
        verbose_name = 'Exterior service card'
        verbose_name_plural = 'Exterior service cards'


# ------------------------------------------------------------------
# PROJECT SHOWCASE GALLERIES (Interior Projects, and later Exterior)
# ------------------------------------------------------------------
class BaseProjectSection(SingletonModel):
    section_label = models.CharField('Small heading', max_length=60, default='Showcase')
    heading = models.CharField('Main heading', max_length=100)
    description = models.CharField('Description', max_length=255, blank=True)

    class Meta:
        abstract = True


class BaseProjectItem(OrderedModel):
    SIZE_NORMAL, SIZE_WIDE, SIZE_TALL = 'normal', 'wide', 'tall'
    SIZE_CHOICES = [
        (SIZE_NORMAL, 'Normal (1 box)'),
        (SIZE_WIDE, 'Wide (2 boxes across)'),
        (SIZE_TALL, 'Tall (2 boxes down)'),
    ]

    title = models.CharField('Room / project name', max_length=80)
    image = models.ImageField('Image', upload_to='projects/', blank=True, null=True)
    size = models.CharField(
        'Tile size', max_length=10, choices=SIZE_CHOICES, default=SIZE_NORMAL,
        help_text='Controls the shape of the photo in the gallery grid. '
                  'The number (01, 02…) is added automatically from the display order.',
    )

    class Meta(OrderedModel.Meta):
        abstract = True

    def __str__(self):
        return self.title


class InteriorProjectSection(BaseProjectSection):
    class Meta:
        verbose_name = 'Interior Projects Gallery'
        verbose_name_plural = 'Interior Projects Gallery'

    def __str__(self):
        return 'Interior Projects Gallery'


class InteriorProject(BaseProjectItem):
    section = models.ForeignKey(InteriorProjectSection, on_delete=models.CASCADE,
                                related_name='projects', default=1)

    class Meta(BaseProjectItem.Meta):
        verbose_name = 'Interior project photo'
        verbose_name_plural = 'Interior project photos'


# ------------------------------------------------------------------
# NUMBERED LIST SECTIONS (Why Choose Us, Our Process)
# ------------------------------------------------------------------
class BaseNumberedSection(SingletonModel):
    section_label = models.CharField('Small heading', max_length=60)
    heading = models.CharField('Main heading', max_length=150)

    class Meta:
        abstract = True


class BaseNumberedItem(OrderedModel):
    title = models.CharField('Title', max_length=80)
    description = models.CharField(
        'Description', max_length=255,
        help_text='The number (01, 02…) is added automatically from the display order.',
    )

    class Meta(OrderedModel.Meta):
        abstract = True

    def __str__(self):
        return self.title


class WhyChooseSection(BaseNumberedSection):
    class Meta:
        verbose_name = 'Why Choose Us Section'
        verbose_name_plural = 'Why Choose Us Section'

    def __str__(self):
        return 'Why Choose Us Section'


class WhyChooseItem(BaseNumberedItem):
    section = models.ForeignKey(WhyChooseSection, on_delete=models.CASCADE,
                                related_name='items', default=1)

    class Meta(BaseNumberedItem.Meta):
        verbose_name = 'Reason'
        verbose_name_plural = 'Reasons (numbered cards)'


class ProcessSection(BaseNumberedSection):
    class Meta:
        verbose_name = 'Our Process Section'
        verbose_name_plural = 'Our Process Section'

    def __str__(self):
        return 'Our Process Section'


class ProcessStep(BaseNumberedItem):
    section = models.ForeignKey(ProcessSection, on_delete=models.CASCADE,
                                related_name='steps', default=1)

    class Meta(BaseNumberedItem.Meta):
        verbose_name = 'Process step'
        verbose_name_plural = 'Process steps'


# ------------------------------------------------------------------
# PORTFOLIO (Our Projects with filter buttons)
# ------------------------------------------------------------------
class PortfolioSection(SingletonModel):
    section_label = models.CharField('Small heading', max_length=60, default='Portfolio')
    heading = models.CharField('Main heading', max_length=100, default='Our Projects')
    all_filter_text = models.CharField('"All" button text', max_length=30, default='All')

    class Meta:
        verbose_name = 'Our Projects Section'
        verbose_name_plural = 'Our Projects Section'

    def __str__(self):
        return 'Our Projects Section'


class ProjectCategory(OrderedModel):
    section = models.ForeignKey(PortfolioSection, on_delete=models.CASCADE,
                                related_name='categories', default=1)
    name = models.CharField('Category name', max_length=50,
                            help_text='Shown as a filter button and as the small label on each project.')
    slug = models.SlugField(max_length=60, unique=True, editable=False)

    class Meta(OrderedModel.Meta):
        verbose_name = 'Filter category'
        verbose_name_plural = 'Filter categories (buttons)'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        base = slugify(self.name) or 'category'
        slug, n = base, 2
        while ProjectCategory.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug, n = f'{base}-{n}', n + 1
        self.slug = slug
        super().save(*args, **kwargs)


class PortfolioProject(OrderedModel):
    category = models.ForeignKey(ProjectCategory, on_delete=models.PROTECT,
                                 related_name='projects', verbose_name='Category')
    title = models.CharField('Project name', max_length=100)
    subtitle = models.CharField('Project type', max_length=60, blank=True, default='Residential',
                                help_text='e.g. Residential, Office, Retail')
    image = models.ImageField('Cover image', upload_to='portfolio/', blank=True, null=True)

    class Meta(OrderedModel.Meta):
        verbose_name = 'Project'
        verbose_name_plural = 'Our Projects — project list'

    def __str__(self):
        return self.title


class PortfolioProjectImage(OrderedModel):
    project = models.ForeignKey(PortfolioProject, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('Image', upload_to='portfolio/gallery/')
    caption = models.CharField('Caption', max_length=150, blank=True)

    class Meta(OrderedModel.Meta):
        verbose_name = 'Extra photo'
        verbose_name_plural = 'Extra photos (opened when the arrow is clicked)'

    def __str__(self):
        return self.caption or f'Photo {self.display_order}'


# ------------------------------------------------------------------
# TESTIMONIALS
# ------------------------------------------------------------------
class TestimonialSection(SingletonModel):
    section_label = models.CharField('Small heading', max_length=60, default='Testimonials')
    heading = models.CharField('Main heading', max_length=100, default='Words from our clients')

    class Meta:
        verbose_name = 'Testimonials Section'
        verbose_name_plural = 'Testimonials Section'

    def __str__(self):
        return 'Testimonials Section'


class Testimonial(OrderedModel):
    section = models.ForeignKey(TestimonialSection, on_delete=models.CASCADE,
                                related_name='testimonials', default=1)
    quote = models.TextField('Client review', help_text='Quotation marks are added automatically.')
    client_name = models.CharField('Client name / role', max_length=80,
                                   help_text='e.g. Homeowner, Business Owner, or the client’s name.')
    project_type = models.CharField('Work done', max_length=80, blank=True,
                                    help_text='e.g. Kitchen & Wardrobes')

    class Meta(OrderedModel.Meta):
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'

    def __str__(self):
        return f'{self.client_name} — {self.project_type}' if self.project_type else self.client_name


# ------------------------------------------------------------------
# CALL-TO-ACTION BANNER ("Start Today")
# ------------------------------------------------------------------
class CTASection(SingletonModel):
    section_label = models.CharField('Small heading', max_length=60, default='Start Today')
    heading = models.CharField('Main heading', max_length=150,
                               default='Let’s Create A Space You’ll Love')
    background_image = models.ImageField(
        'Background image', upload_to='cta/', blank=True, null=True,
        help_text='Wide landscape photo (at least 1920px wide). A dark overlay is added automatically.',
    )
    primary_button_text = models.CharField(
        'Main button text', max_length=50, default='Get a Quote',
        help_text='Scrolls to the Contact section.',
    )
    secondary_button_text = models.CharField(
        'Second button text', max_length=50, default='Contact Us',
        help_text='Scrolls to the Contact section.',
    )

    class Meta:
        verbose_name = 'Start Today Banner'
        verbose_name_plural = 'Start Today Banner'

    def __str__(self):
        return 'Start Today Banner'


# ------------------------------------------------------------------
# CONTACT SECTION + ENQUIRIES
# ------------------------------------------------------------------
class ContactSection(SingletonModel):
    section_label = models.CharField('Small heading', max_length=60, default='Contact')
    heading = models.CharField('Main heading', max_length=150, default='Tell us about your space')
    description = models.CharField(
        'Description', max_length=255,
        default='Share a few details and our team will get back within one working day.',
    )

    address = models.TextField('Address', blank=True)
    phone_numbers = models.CharField(
        'Phone numbers', max_length=100, blank=True,
        help_text='Separate multiple numbers with a comma. Each one becomes a tap-to-call link.',
    )
    email = models.EmailField('Email', blank=True)
    instagram_handle = models.CharField(
        'Instagram username', max_length=60, blank=True,
        help_text='Without the @, e.g. classic_Comfort_interior',
    )

    # Form texts
    form_button_text = models.CharField('Form button text', max_length=40, default='Send Enquiry')
    service_placeholder = models.CharField('Service dropdown text', max_length=60, default='Service Required')
    success_message = models.CharField(
        'Message after sending', max_length=255,
        default='Thank you! Our team will get back to you within one working day.',
    )

    class Meta:
        verbose_name = 'Contact Section'
        verbose_name_plural = 'Contact Section'

    def __str__(self):
        return 'Contact Section'

    @property
    def phone_list(self):
        """[(display, tel_link_number), ...]"""
        result = []
        for raw in self.phone_numbers.split(','):
            raw = raw.strip()
            if not raw:
                continue
            digits = ''.join(ch for ch in raw if ch.isdigit())
            if len(digits) == 10:
                digits = '91' + digits
            result.append((raw, f'+{digits}'))
        return result

    @property
    def instagram_url(self):
        handle = self.instagram_handle.strip().lstrip('@')
        return f'https://www.instagram.com/{handle}/' if handle else ''

    @property
    def map_url(self):
        from urllib.parse import quote_plus
        return f'https://www.google.com/maps/search/?api=1&query={quote_plus(self.address)}' if self.address else ''


class Enquiry(models.Model):
    STATUS_NEW, STATUS_CONTACTED, STATUS_CLOSED = 'new', 'contacted', 'closed'
    STATUS_CHOICES = [
        (STATUS_NEW, 'New'),
        (STATUS_CONTACTED, 'Contacted'),
        (STATUS_CLOSED, 'Closed'),
    ]

    name = models.CharField('Name', max_length=100)
    phone = models.CharField('Phone', max_length=20)
    email = models.EmailField('Email')
    service = models.CharField('Service required', max_length=120)
    message = models.TextField('Message')

    status = models.CharField('Status', max_length=12, choices=STATUS_CHOICES, default=STATUS_NEW)
    notes = models.TextField('Internal notes', blank=True, help_text='Only visible in the admin.')
    email_sent = models.BooleanField('Email notification sent', default=False, editable=False)
    ip_address = models.GenericIPAddressField('IP address', blank=True, null=True, editable=False)
    created_at = models.DateTimeField('Received on', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Enquiry'
        verbose_name_plural = 'Enquiries (from contact form)'

    def __str__(self):
        return f'{self.name} — {self.service}'


# ------------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------------
class FooterSettings(SingletonModel):
    footer_logo = models.ImageField(
        'Footer logo', upload_to='site/', blank=True, null=True,
        help_text='Optional light version of the logo for the dark footer. '
                  'Leave blank to use the main logo from Website Settings.',
    )
    about_text = models.CharField(
        'Short description', max_length=255,
        default='Interior, exterior and commercial works — designed and built with care.',
    )
    follow_text = models.CharField('Social media heading', max_length=60, default='Follow us,')

    quick_links_title = models.CharField('Column 1 heading', max_length=40, default='Quick Links',
                                         help_text='Links come from "Navbar Menu Links".')
    interior_title = models.CharField('Column 2 heading', max_length=40, default='Interior',
                                      help_text='Links come from the Interior service cards.')
    exterior_title = models.CharField('Column 3 heading', max_length=40, default='Exterior',
                                      help_text='Links come from the Exterior service cards.')
    contact_title = models.CharField('Column 4 heading', max_length=40, default='Contact',
                                     help_text='Address, phone and email come from "Contact Section".')

    copyright_text = models.CharField(
        'Copyright text', max_length=150, default='All rights reserved.',
        help_text='Shown as: © <current year> <company name>. <this text>',
    )

    credit_prefix = models.CharField('Credit text', max_length=80, default='Designed & Developed by')
    credit_name = models.CharField('Developer name', max_length=80, default='Vetri IT Systems')
    credit_url = models.URLField('Developer website', default='https://vetriitsystems.com/',
                                 help_text='The developer name links here (opens in a new tab).')

    class Meta:
        verbose_name = 'Footer'
        verbose_name_plural = 'Footer'

    def __str__(self):
        return 'Footer'


class SocialLink(OrderedModel):
    PLATFORM_CHOICES = [
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('youtube', 'YouTube'),
        ('whatsapp', 'WhatsApp'),
        ('linkedin', 'LinkedIn'),
        ('x', 'X (Twitter)'),
        ('pinterest', 'Pinterest'),
    ]

    footer = models.ForeignKey(FooterSettings, on_delete=models.CASCADE, related_name='social_links', default=1)
    platform = models.CharField('Platform', max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField('Page link', blank=True,
                          help_text='Full link to the page. Icons without a link are hidden on the website.')

    class Meta(OrderedModel.Meta):
        verbose_name = 'Social media link'
        verbose_name_plural = 'Social media links'

    def __str__(self):
        return self.get_platform_display()


# ------------------------------------------------------------------
# FLOATING CONTACT BUTTONS (WhatsApp / call / Instagram, bottom-right)
# ------------------------------------------------------------------
class FloatingButtons(SingletonModel):
    show_call = models.BooleanField('Show call button', default=True)
    call_number = models.CharField('Call number', max_length=20, default='6374851724',
                                   help_text='10-digit mobile number. +91 is added automatically.')

    show_whatsapp = models.BooleanField('Show WhatsApp button', default=True)
    whatsapp_number = models.CharField('WhatsApp number', max_length=20, default='6374851724',
                                       help_text='10-digit mobile number. +91 is added automatically.')
    whatsapp_message = models.CharField(
        'WhatsApp starting message', max_length=200, blank=True,
        default='Hi, I would like to know more about your interior and exterior services.',
        help_text='Pre-filled text when the chat opens. Leave blank for an empty chat.',
    )

    show_instagram = models.BooleanField('Show Instagram button', default=True)
    instagram_url = models.URLField('Instagram page link',
                                    default='https://www.instagram.com/classic_Comfort_interior/')

    class Meta:
        verbose_name = 'Floating Contact Buttons'
        verbose_name_plural = 'Floating Contact Buttons'

    def __str__(self):
        return 'Floating Contact Buttons'

    @staticmethod
    def _intl(number):
        digits = ''.join(ch for ch in number if ch.isdigit())
        return '91' + digits if len(digits) == 10 else digits

    @property
    def tel_link(self):
        return f'tel:+{self._intl(self.call_number)}' if self.call_number else ''

    @property
    def whatsapp_link(self):
        from urllib.parse import quote
        if not self.whatsapp_number:
            return ''
        link = f'https://wa.me/{self._intl(self.whatsapp_number)}'
        return f'{link}?text={quote(self.whatsapp_message)}' if self.whatsapp_message else link


# ------------------------------------------------------------------
# EMAIL / SMTP SETTINGS (managed only from admin, never .env)
# ------------------------------------------------------------------
class EmailSettings(SingletonModel):
    smtp_host = models.CharField('SMTP server', max_length=200, blank=True,
                                 help_text='e.g. smtp.gmail.com')
    smtp_port = models.PositiveIntegerField('SMTP port', default=587,
                                            help_text='587 for TLS, 465 for SSL.')
    use_tls = models.BooleanField('Use TLS', default=True)
    use_ssl = models.BooleanField('Use SSL', default=False)
    smtp_username = models.CharField('Email login (username)', max_length=200, blank=True)
    smtp_password = models.CharField(
        'Email password / App password', max_length=200, blank=True,
        help_text='For Gmail, create an "App Password" in your Google account security settings.',
    )
    from_email = models.EmailField('Send emails from', blank=True,
                                   help_text='Usually the same as the email login.')
    notify_email = models.EmailField(
        'Send enquiries to', blank=True,
        help_text='Quote / contact form enquiries are delivered to this address.',
    )

    # Confirmation email to the person who filled in the form
    send_auto_reply = models.BooleanField(
        'Send confirmation email to the customer', default=True,
        help_text='After a form is submitted, the customer receives a thank-you email.',
    )
    auto_reply_subject = models.CharField(
        'Confirmation email subject', max_length=150,
        default='Thank you for contacting Classic Comfort Interior and Exterior',
    )
    auto_reply_message = models.TextField(
        'Confirmation email message',
        default='Thank you for reaching out to us. We have received your enquiry and our team '
                'will get back to you within one working day.\n\n'
                'Warm regards,\nClassic Comfort Interior and Exterior',
        help_text='"Hi <name>," is added at the top and a summary of their enquiry at the bottom.',
    )

    class Meta:
        verbose_name = 'Email (SMTP) Settings'
        verbose_name_plural = 'Email (SMTP) Settings'

    def __str__(self):
        return 'Email (SMTP) Settings'

    def clean(self):
        if self.use_tls and self.use_ssl:
            raise ValidationError('Choose either TLS or SSL, not both.')

    @property
    def is_configured(self):
        return bool(self.smtp_host and self.smtp_username and self.smtp_password)
