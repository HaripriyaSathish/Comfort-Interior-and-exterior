from django.core.management.base import BaseCommand

from core.models import (
    AboutPromise, AboutSection, AboutWorkType, ContactSection, CTASection, EmailSettings, FloatingButtons, FooterSettings, ExteriorSection, ExteriorService,
    HeroSection, InteriorProject,
    InteriorProjectSection, InteriorSection, InteriorService, NavMenuItem, PortfolioProject,
    PortfolioSection, ProcessSection, ProcessStep, ProjectCategory, SiteSettings, SocialLink, Testimonial,
    TestimonialSection, WhyChooseItem, WhyChooseSection,
)

# Navbar follows the order of sections on the page.
NAV_ITEMS = [
    ('Home', 'home'),
    ('About', 'about'),
    ('Interior', 'interior'),
    ('Exterior', 'exterior'),
    ('Projects', 'projects'),
    ('Contact', 'contact'),
]

# *word* = gold highlight, _word_ = italic, blank line = new paragraph
ABOUT = {
    'section_label': 'About Us',
    'intro': 'At *Classic Comfort Interior and Exterior*, we believe every space has a story to tell.',
    'content': (
        'We are a passionate interior and exterior design company dedicated to transforming houses, '
        'offices, and commercial spaces into beautiful, functional, and comfortable environments. '
        'From concept to completion, we focus on understanding our clients’ needs, lifestyle, '
        'and vision to create spaces that truly feel like their own.\n\n'
        'Our expertise includes *Modular Kitchens, Bedroom Interiors, Living Room Interiors, '
        'Residential Exteriors, and Commercial Interior Projects*.\n\n'
        'With a strong focus on *quality, creativity, functionality, and attention to detail*, '
        'we work closely with our clients throughout every stage of the project — from planning '
        'and material selection to execution and final finishing.'
    ),
    'closing_text': (
        'At Classic Comfort, we don’t just design spaces.\n'
        '_We turn spaces into stories and dreams into beautiful homes._'
    ),
    'vision_title': 'Our Vision',
    'vision_text': '_Crafting your space, Crafting memories_',
    'promise_title': 'Our Promise',
}

ABOUT_WORK_TYPES = [
    ('Interior', 'Works', 'interior'),
    ('Exterior', 'Works', 'exterior'),
    ('Commercial', 'Works', 'exterior'),
]

ABOUT_PROMISES = ['Quality', 'Transparency', 'Creativity', 'On-Time Execution', 'Client Satisfaction']

INTERIOR = {
    'section_label': 'What We Do Inside',
    'heading': 'Interior Works',
    'description': 'Every element of your home — designed, manufactured and installed by our own team.',
    'enquire_button_text': 'Enquire',
}

INTERIOR_SERVICES = [
    ('Kitchen Interior', 'Modular kitchens planned for flow, storage and lasting finishes.'),
    ('Wardrobes', 'Sliding, hinged and walk-in wardrobes tailored to every inch.'),
    ('TV Unit', 'Feature walls and media units with integrated lighting.'),
    ('Puja Unit', 'Serene, crafted mandir units in wood, jali and brass.'),
    ('Panelling Work', 'Fluted, upholstered and veneer wall panelling.'),
    ('False Ceiling', 'Gypsum and POP ceilings with layered cove lighting.'),
    ('Flooring', 'Wood, marble, vinyl and tile flooring installed with precision.'),
    ('Wallpaper', 'Curated textures and murals for statement walls.'),
]

INTERIOR_GALLERY = {
    'section_label': 'Showcase',
    'heading': 'Interior Projects',
    'description': 'A look at rooms we’ve recently completed.',
}

# Order matches the numbers 01-06 in the design; size sets the tile shape in the grid.
INTERIOR_PROJECTS = [
    ('Kitchen', 'wide'),
    ('Living Room', 'tall'),
    ('Bedroom', 'normal'),
    ('Wardrobe', 'normal'),
    ('TV Unit', 'normal'),
    ('False Ceiling', 'wide'),
]

EXTERIOR = {
    'section_label': 'Facades & Brands',
    'heading': 'Exterior & Commercial Works',
    'description': 'Durable, beautifully detailed facades and signage that make a strong first impression.',
    'enquire_button_text': 'Enquire',
}

EXTERIOR_SERVICES = [
    ('Exterior Elevation Board', 'Facade elevations in stone, HPL and louvers that define arrival.'),
    ('Sign Board', '3D lit letters, LED and metal signage for brands.'),
    ('Flex Works', 'Large-format flex printing and framed installations.'),
    ('Curtain Wall Glass Works', 'Structural and semi-unitized glazing systems.'),
    ('ACP Work', 'Aluminium composite cladding for clean, durable facades.'),
]

WHY_CHOOSE = {'section_label': 'Why Choose Us', 'heading': 'Built on detail and trust'}

WHY_CHOOSE_ITEMS = [
    ('Custom Design', 'Every layout and finish is drawn for your space, your routine and your taste.'),
    ('Quality Materials', 'Branded boards, hardware and glass, chosen for how they age — not just how they look.'),
    ('Skilled Workmanship', 'Experienced in-house craftsmen with tight finishing standards on every joint.'),
    ('On-Time Execution', 'Clear schedules, weekly updates and a single point of contact until handover.'),
]

PROCESS = {'section_label': 'Our Process', 'heading': 'From first visit to final handover'}

PROCESS_STEPS = [
    ('Consultation', 'We visit, listen and understand your needs and budget.'),
    ('Design & Planning', '2D layouts, 3D views and a detailed scope.'),
    ('Material Selection', 'Finishes, hardware and samples chosen together.'),
    ('Execution', 'Manufacturing and installation by our team.'),
    ('Final Handover', 'Quality check, cleaning and walkthrough.'),
]

PORTFOLIO = {'section_label': 'Portfolio', 'heading': 'Our Projects', 'all_filter_text': 'All'}

PROJECT_CATEGORIES = ['Interior', 'Exterior', 'Commercial']

# (category, title, project type)
PORTFOLIO_PROJECTS = [
    ('Interior', 'Modular Kitchen', 'Residential'),
    ('Interior', 'TV Unit cum Puja Unit', 'Residential'),
    ('Interior', 'Wardrobe', 'Residential'),
    ('Interior', 'Wardrobe', 'Residential'),
    ('Interior', 'Wardrobe', 'Residential'),
    ('Interior', 'Wardrobe', 'Residential'),
    ('Interior', 'Modular Kitchen', 'Residential'),
    ('Interior', 'Modular Kitchen', 'Residential'),
    ('Interior', 'Modular Kitchen', 'Residential'),
]

TESTIMONIAL_SECTION = {'section_label': 'Testimonials', 'heading': 'Words from our clients'}

TESTIMONIALS = [
    ('The kitchen and wardrobes came out exactly like the 3D views. '
     'The team was patient with every change we asked for.', 'Homeowner', 'Kitchen & Wardrobes'),
    ('They handled our office facade and lobby together, which saved us a lot of coordination. '
     'Clean, professional work.', 'Business Owner', 'Commercial Fit-out'),
    ('Our false ceiling and TV wall transformed the living room. '
     'Neat finishing and the site was left spotless.', 'Homeowner', 'Living Room'),
]

CONTACT = {
    'address': 'No 5, Ganesh nagar, ayapakkam, Chennai 600077',
    'phone_numbers': '6374851724, 8525896731',
    'email': 'classiccomfortinteriorexterior@gmail.com',
    'instagram_handle': 'classic_Comfort_interior',
}

SOCIAL_LINKS = [
    ('instagram', 'https://www.instagram.com/classic_Comfort_interior/'),
    ('facebook', ''),  # add the Facebook page link in admin to show the icon
]

# Gmail SMTP for the business address. The App Password is never seeded —
# the client enters it in Admin → Email (SMTP) Settings.
BUSINESS_EMAIL = 'classiccomfortinteriorexterior@gmail.com'
EMAIL_SETTINGS = {
    'smtp_host': 'smtp.gmail.com',
    'smtp_port': 587,
    'use_tls': True,
    'use_ssl': False,
    'smtp_username': BUSINESS_EMAIL,
    'from_email': BUSINESS_EMAIL,
    'notify_email': BUSINESS_EMAIL,
}


class Command(BaseCommand):
    help = 'Fill the database with the default website content. Existing content is never overwritten.'

    def handle(self, *args, **options):
        SiteSettings.load()
        HeroSection.load()
        CTASection.load()
        FloatingButtons.load()
        email_cfg = EmailSettings.load()
        changed = False
        for field, value in EMAIL_SETTINGS.items():
            if field in ('smtp_port', 'use_tls', 'use_ssl'):
                continue  # model defaults already match Gmail (587 / TLS)
            if not getattr(email_cfg, field):  # only fill blanks, never overwrite admin edits
                setattr(email_cfg, field, value)
                changed = True
        if changed:
            email_cfg.save()

        for order, (label, section) in enumerate(NAV_ITEMS, start=1):
            NavMenuItem.objects.get_or_create(
                section=section, defaults={'label': label, 'display_order': order},
            )

        about, created = AboutSection.objects.get_or_create(pk=1, defaults=ABOUT)
        if created or not about.work_types.exists():
            for order, (title, subtitle, section) in enumerate(ABOUT_WORK_TYPES, start=1):
                AboutWorkType.objects.create(
                    about=about, title=title, subtitle=subtitle, section=section, display_order=order,
                )
        if created or not about.promises.exists():
            for order, text in enumerate(ABOUT_PROMISES, start=1):
                AboutPromise.objects.create(about=about, text=text, display_order=order)

        interior, created = InteriorSection.objects.get_or_create(pk=1, defaults=INTERIOR)
        if created or not interior.services.exists():
            for order, (title, description) in enumerate(INTERIOR_SERVICES, start=1):
                InteriorService.objects.create(
                    section=interior, title=title, description=description, display_order=order,
                )

        gallery, created = InteriorProjectSection.objects.get_or_create(pk=1, defaults=INTERIOR_GALLERY)
        if created or not gallery.projects.exists():
            for order, (title, size) in enumerate(INTERIOR_PROJECTS, start=1):
                InteriorProject.objects.create(section=gallery, title=title, size=size, display_order=order)

        exterior, created = ExteriorSection.objects.get_or_create(pk=1, defaults=EXTERIOR)
        if created or not exterior.services.exists():
            for order, (title, description) in enumerate(EXTERIOR_SERVICES, start=1):
                ExteriorService.objects.create(
                    section=exterior, title=title, description=description, display_order=order,
                )

        why, created = WhyChooseSection.objects.get_or_create(pk=1, defaults=WHY_CHOOSE)
        if created or not why.items.exists():
            for order, (title, description) in enumerate(WHY_CHOOSE_ITEMS, start=1):
                WhyChooseItem.objects.create(section=why, title=title, description=description, display_order=order)

        process, created = ProcessSection.objects.get_or_create(pk=1, defaults=PROCESS)
        if created or not process.steps.exists():
            for order, (title, description) in enumerate(PROCESS_STEPS, start=1):
                ProcessStep.objects.create(section=process, title=title, description=description, display_order=order)

        portfolio, created = PortfolioSection.objects.get_or_create(pk=1, defaults=PORTFOLIO)
        if created or not portfolio.categories.exists():
            for order, name in enumerate(PROJECT_CATEGORIES, start=1):
                ProjectCategory.objects.create(section=portfolio, name=name, display_order=order)
        if not PortfolioProject.objects.exists():
            categories = {c.name: c for c in portfolio.categories.all()}
            for order, (category, title, subtitle) in enumerate(PORTFOLIO_PROJECTS, start=1):
                PortfolioProject.objects.create(
                    category=categories[category], title=title, subtitle=subtitle, display_order=order,
                )

        reviews, created = TestimonialSection.objects.get_or_create(pk=1, defaults=TESTIMONIAL_SECTION)
        if created or not reviews.testimonials.exists():
            for order, (quote, client_name, project_type) in enumerate(TESTIMONIALS, start=1):
                Testimonial.objects.create(
                    section=reviews, quote=quote, client_name=client_name,
                    project_type=project_type, display_order=order,
                )

        ContactSection.objects.get_or_create(pk=1, defaults=CONTACT)

        footer, created = FooterSettings.objects.get_or_create(pk=1)
        if created or not footer.social_links.exists():
            for order, (platform, url) in enumerate(SOCIAL_LINKS, start=1):
                SocialLink.objects.create(footer=footer, platform=platform, url=url, display_order=order)

        self.stdout.write(self.style.SUCCESS('Seed data created. Upload images from the admin panel.'))
