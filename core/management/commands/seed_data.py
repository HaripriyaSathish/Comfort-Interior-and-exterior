from django.core.management.base import BaseCommand

from core.models import (
    AboutPromise, AboutSection, AboutWorkType, ContactSection, CTASection, EmailSettings, EnquiryService, FAQItem, FAQSection, FloatingButtons, FooterSettings, ExteriorSection, ExteriorService,
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
# SEO copy, sections 3.2 About Us and 3.3 Our Promise.
ABOUT = {
    'section_label': 'About Us',
    'heading': 'A Trusted Interior Design Company for Homes, Offices and Exteriors',
    'intro': '',
    'content': (
        'Classic Comfort Interior & Exterior is an interior design company that helps homeowners '
        'and business owners turn plain spaces into well-planned, comfortable ones. Our interior '
        'designers begin every project by studying how the space will be used, so the final result '
        'suits your routine, your family and your budget.\n\n'
        'Our interior design services cover the whole project: layout planning, 3D views, material '
        'selection, manufacturing, installation and final finishing. Because our interior works are '
        'handled by one team, you get a single point of contact and better control over quality '
        'and timelines.\n\n'
        'At home, we specialise in residential interior design, including modular kitchens, bedroom '
        'interior design and living room interior design, along with wardrobes, TV units, false '
        'ceilings and wall panelling. For businesses, we deliver office interior design and '
        'commercial interior design for shops, showrooms and workspaces.\n\n'
        'Our work also extends outside. From exterior house design to facade cladding, we make sure '
        'the outside of your building matches the quality of the inside.\n\n'
        'Looking for interior designers who listen first and build with care? Get a quote and '
        'let’s plan your space together.'
    ),
    'closing_text': '',
    'mission_title': 'Our Mission',
    'mission_text': (
        'To deliver reliable interior design services for homes, offices and exteriors, with clear '
        'planning, quality materials and on-time execution, so every client gets a space that is '
        'comfortable, functional and built to last.'
    ),
    'vision_title': 'Our Vision',
    'vision_text': (
        'To be the interior design company people recommend for honest planning, neat finishing '
        'and spaces that stay comfortable for years.'
    ),
    'promise_title': 'Our Promise',
}
# Earlier seeded values; these are replaced, anything else typed in admin is kept.
OLD_ABOUT = {
    'section_label': 'About Us',
    'heading': '',
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
    'mission_title': 'Our Mission',
    'mission_text': '',
    'vision_title': 'Our Vision',
    'vision_text': '_Crafting your space, Crafting memories_',
    'promise_title': 'Our Promise',
}

ABOUT_WORK_TYPES = [
    ('Interior', 'Works', 'interior'),
    ('Exterior', 'Works', 'exterior'),
    ('Commercial', 'Interiors', 'exterior'),
]
# (title, old subtitle, new subtitle) for rows seeded earlier
ABOUT_WORK_TYPE_RENAMES = [('Commercial', 'Works', 'Interiors')]

ABOUT_PROMISES = ['Quality', 'Transparency', 'Creative Design', 'On-Time Execution', 'Client Satisfaction']
ABOUT_PROMISE_RENAMES = [('Creativity', 'Creative Design')]

# SEO copy, section 3.4 — Interior Works.
INTERIOR = {
    'section_label': 'What We Do Inside',
    'heading': 'Complete Interior Works for Every Space',
    'description': (
        'Our interior solutions are planned to make every part of your space more functional '
        'and visually appealing.'
    ),
    'enquire_button_text': 'Enquire',
}
OLD_INTERIOR = {
    'section_label': 'What We Do Inside',
    'heading': 'Interior Works',
    'description': 'Every element of your home — designed, manufactured and installed by our own team.',
    'enquire_button_text': 'Enquire',
}

INTERIOR_SERVICES = [
    ('Kitchen Interior Design',
     'From layout planning to finishes and storage, our kitchen interior design solutions combine '
     'functionality with a refined appearance.'),
    ('Wardrobe Design',
     'Make the most of your space with customised wardrobe design solutions that provide practical '
     'storage and a clean, modern look.'),
    ('TV Unit Design',
     'Create a stylish focal point with functional TV unit design solutions that complement your '
     'living space.'),
    ('Puja Unit Design',
     'Elegant and functional puja unit designs customised to complement your home interiors, '
     'combining traditional charm with modern style.'),
    ('Wall Panelling',
     'Add character and depth to your interiors with carefully selected wall panelling solutions.'),
    ('False Ceiling',
     'Enhance the overall appearance of your interiors with professionally planned false ceiling designs.'),
    ('Flooring Solutions',
     'Get practical and visually appealing flooring solutions planned to complement your overall '
     'interior design.'),
    ('Wallpaper Installation',
     'Refresh your interiors with professional wallpaper installation for selected walls and spaces.'),
]
# Earlier seeded cards, same order; a card still holding this exact text is updated.
OLD_INTERIOR_SERVICES = [
    ('Kitchen Interior', 'Modular kitchens planned for flow, storage and lasting finishes.'),
    ('Wardrobes', 'Sliding, hinged and walk-in wardrobes tailored to every inch.'),
    ('TV Unit', 'Feature walls and media units with integrated lighting.'),
    ('Puja Unit', 'Serene, crafted mandir units in wood, jali and brass.'),
    ('Panelling Work', 'Fluted, upholstered and veneer wall panelling.'),
    ('False Ceiling', 'Gypsum and POP ceilings with layered cove lighting.'),
    ('Flooring', 'Wood, marble, vinyl and tile flooring installed with precision.'),
    ('Wallpaper', 'Curated textures and murals for statement walls.'),
]

# SEO copy, section 3.5 — Interior Showcase heading.
INTERIOR_GALLERY = {
    'section_label': 'Showcase',
    'heading': 'Designed Spaces. Thoughtful Details.',
    'description': (
        'Explore our interior design approach, creating stylish and functional spaces with thoughtful '
        'details. From living rooms and kitchens to wardrobes, TV units and wall finishes, every '
        'element is designed to suit your lifestyle and needs.'
    ),
}
OLD_INTERIOR_GALLERY = {
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

# SEO copy, section 3.6 — Exterior & Commercial Works.
EXTERIOR = {
    'section_label': 'Facades & Brands',
    'heading': 'Exterior House Design and Commercial Facade Works',
    'description': (
        'From house elevation design and facade cladding to ACP wall cladding and signage, '
        'we give homes and commercial buildings a durable, polished look.'
    ),
    'enquire_button_text': 'Enquire',
}
OLD_EXTERIOR = {
    'section_label': 'Facades & Brands',
    'heading': 'Exterior & Commercial Works',
    'description': 'Durable, beautifully detailed facades and signage that make a strong first impression.',
    'enquire_button_text': 'Enquire',
}

EXTERIOR_SERVICES = [
    ('Exterior Elevation Board',
     'House elevation design in stone, HPL and louvers that gives your home a strong first impression.'),
    ('Sign Board', '3D lit letters, LED and metal sign boards that give your brand a clear identity.'),
    ('Flex Works', 'Large-format flex printing and framed installations for shops, offices and showrooms.'),
    ('Curtain Wall Glass Works',
     'Structural and semi-unitized curtain wall glazing for modern commercial buildings.'),
    ('ACP Work', 'ACP wall cladding and facade cladding for clean, weather-resistant exteriors.'),
]
# Earlier seeded cards, same order; a card still holding this exact text is updated.
OLD_EXTERIOR_SERVICES = [
    ('Exterior Elevation Board', 'Facade elevations in stone, HPL and louvers that define arrival.'),
    ('Sign Board', '3D lit letters, LED and metal signage for brands.'),
    ('Flex Works', 'Large-format flex printing and framed installations.'),
    ('Curtain Wall Glass Works', 'Structural and semi-unitized glazing systems.'),
    ('ACP Work', 'Aluminium composite cladding for clean, durable facades.'),
]

# SEO copy, section 3.7 — Why Choose Us.
WHY_CHOOSE = {
    'section_label': 'Why Choose Us',
    'heading': 'Why Choose Classic Comfort Interior and Exterior?',
}
OLD_WHY_CHOOSE = {'section_label': 'Why Choose Us', 'heading': 'Built on detail and trust'}

WHY_CHOOSE_ITEMS = [
    ('Thoughtful Design',
     'We create designs based on your space, requirements, lifestyle and functional needs.'),
    ('Complete Interior Solutions',
     'From kitchen interior design and wardrobes to ceilings, wall panelling and living spaces, '
     'we provide a comprehensive approach to interior works.'),
    ('Residential & Commercial Expertise',
     'Our solutions cover residential interior design, office interior design and commercial '
     'interior design requirements.'),
    ('Functional & Aesthetic Approach',
     'We focus on creating spaces that are not only visually appealing but also practical for '
     'everyday use.'),
    ('Attention to Detail',
     'Every element, from layout and storage to finishes and overall presentation, is considered '
     'as part of the complete design.'),
    ('Professional Execution',
     'We aim to bring the approved design concept to life with careful planning and execution.'),
]
# Earlier seeded points, same order; a point still holding this exact text is updated.
OLD_WHY_CHOOSE_ITEMS = [
    ('Custom Design', 'Every layout and finish is drawn for your space, your routine and your taste.'),
    ('Quality Materials', 'Branded boards, hardware and glass, chosen for how they age — not just how they look.'),
    ('Skilled Workmanship', 'Experienced in-house craftsmen with tight finishing standards on every joint.'),
    ('On-Time Execution', 'Clear schedules, weekly updates and a single point of contact until handover.'),
]

# SEO copy, section 3.8 — Our Process. The 01-06 numbers are added on the page.
PROCESS = {'section_label': 'Our Process', 'heading': 'Our Interior Design Process'}
OLD_PROCESS = {'section_label': 'Our Process', 'heading': 'From first visit to final handover'}

PROCESS_STEPS = [
    ('Understand', 'We begin by understanding your space, requirements, preferences and functional needs.'),
    ('Plan', 'Our team develops a design direction based on the available space, usage and desired aesthetics.'),
    ('Design', 'We create detailed interior concepts for areas such as kitchens, bedrooms, living rooms, '
               'offices and other spaces.'),
    ('Finalise', 'Design elements, materials, finishes and requirements are reviewed and finalised.'),
    ('Execute', 'The approved design is implemented with attention to detail and quality.'),
    ('Transform', 'Your planned space is transformed into a functional and visually refined interior.'),
]
# Earlier seeded steps, same order; a step still holding this exact text is updated.
OLD_PROCESS_STEPS = [
    ('Consultation', 'We visit, listen and understand your needs and budget.'),
    ('Design & Planning', '2D layouts, 3D views and a detailed scope.'),
    ('Material Selection', 'Finishes, hardware and samples chosen together.'),
    ('Execution', 'Manufacturing and installation by our team.'),
    ('Final Handover', 'Quality check, cleaning and walkthrough.'),
]

# SEO copy, section 3.9 — Portfolio / Our Projects.
PORTFOLIO = {
    'section_label': 'Portfolio',
    'heading': 'Interior Design Projects for Homes, Offices and Exteriors',
    'description': (
        'Browse our recent interior works, from modular kitchens, wardrobe design and false ceilings '
        'to office interior design and house elevation projects.'
    ),
    'all_filter_text': 'All',
    'all_filter_title': 'All interior design projects',
}
OLD_PORTFOLIO = {
    'section_label': 'Portfolio', 'heading': 'Our Projects', 'description': '',
    'all_filter_text': 'All', 'all_filter_title': '',
}

PROJECT_CATEGORIES = ['Interior', 'Exterior', 'Commercial']
# Hover text (title attribute) of each filter button
PROJECT_CATEGORY_TITLES = {
    'Interior': 'Residential interior design projects',
    'Exterior': 'Exterior house design and facade projects',
    'Commercial': 'Commercial interior design and office projects',
}

# SEO doc's suggested project captions: (category, title, project type, one-line description).
# Used for a fresh site; upload the photos in admin.
PORTFOLIO_PROJECTS = [
    ('Interior', 'Modular Kitchen Design', 'Residential',
     'Island kitchen with tall storage units and soft under-cabinet lighting.'),
    ('Interior', 'Walk-in Wardrobe Design', 'Residential',
     'Glass-shutter wardrobe with loft storage, drawers and a central island.'),
    ('Interior', 'Living Room Interior Design', 'Residential',
     'TV unit, false ceiling and flooring planned as one scheme.'),
    ('Interior', 'Bedroom Interior Design', 'Residential',
     'Upholstered headboard wall panelling with bedside storage.'),
    ('Commercial', 'Office Interior Design', 'Office',
     'Reception, cabins and workstations with glass partitions.'),
    ('Exterior', 'House Elevation Design', 'Residential',
     'Stone, HPL and louver elevation with warm exterior lighting.'),
]
# Existing project cards (real photos) get the caption that matches their photo:
# old title -> (new title, one-line description). Only cards with no description yet.
PORTFOLIO_CAPTIONS = {
    'Modular Kitchen': PORTFOLIO_PROJECTS[0][1:4:2],
    'Wardrobe': PORTFOLIO_PROJECTS[1][1:4:2],
    'TV Unit cum Puja Unit': PORTFOLIO_PROJECTS[2][1:4:2],
}

# SEO copy, section 3.10 — Testimonials.
TESTIMONIAL_SECTION = {
    'section_label': 'Testimonials',
    'heading': 'What Our Clients Say',
    'description': (
        'See why clients choose Classic Comfort Interior and Exterior for thoughtful interior '
        'and exterior design.'
    ),
}
OLD_TESTIMONIAL_SECTION = {'section_label': 'Testimonials', 'heading': 'Words from our clients', 'description': ''}

# SEO copy, section 3.11 — CTA banner.
CTA = {
    'section_label': 'Start Today',
    'heading': 'Ready to Transform Your Space?',
    'description': (
        'Looking for professional interior design services for your home, office or commercial space?\n\n'
        'Connect with Classic Comfort Interior and Exterior to discuss your requirements and explore '
        'a design approach created around your space.'
    ),
    'primary_button_text': 'Start Your Interior Design Journey',
    'secondary_button_text': 'Contact Us',
}
OLD_CTA = {
    'section_label': 'Start Today',
    'heading': 'Let’s Create A Space You’ll Love',
    'description': '',
    'primary_button_text': 'Get a Quote',
    'secondary_button_text': 'Contact Us',
}

TESTIMONIALS = [
    ('The kitchen and wardrobes came out exactly like the 3D views. '
     'The team was patient with every change we asked for.', 'Homeowner', 'Kitchen & Wardrobes'),
    ('They handled our office facade and lobby together, which saved us a lot of coordination. '
     'Clean, professional work.', 'Business Owner', 'Commercial Fit-out'),
    ('Our false ceiling and TV wall transformed the living room. '
     'Neat finishing and the site was left spotless.', 'Homeowner', 'Living Room'),
]

# SEO copy from Classic_Comfort_SEO_Content (Oct 2026), section 2 — Meta Tags.
SITE_SEO = {
    'meta_title': 'Interior Designers in Chennai | Classic Comfort Interior',
    'meta_description': (
        'Classic Comfort Interior & Exterior offers interior design services, modular kitchens, '
        'wardrobes, false ceilings and facade works. Get a quote today.'
    ),
}
# Earlier seeded values; these are replaced, anything else typed in admin is kept.
OLD_SITE_SEO = {
    'meta_title': 'Classic Comfort Interior and Exterior | Interior, Exterior & Commercial Design',
    'meta_description': (
        'From bespoke kitchens and wardrobes to striking facades and commercial fit-outs, '
        'Classic Comfort designs and builds every detail, end to end.'
    ),
}

# SEO copy, section 3.1 — Hero Section.
HERO = {
    'tagline': 'Interior · Exterior · Commercial',
    'heading': 'Crafting Spaces That Feel Like Home',
    'description': (
        'Planning a new home or revamping an office? Our interior design services cover '
        'everything from a modular kitchen to a full commercial fit-out, with one team '
        'handling design, work and finishing.'
    ),
    'primary_button_text': 'View Interior Works',
    'secondary_button_text': 'Request a Quote',
}
OLD_HERO = {
    'tagline': 'Interior • Exterior • Commercial',
    'heading': 'Crafting Spaces That Feel Like Home',
    'description': (
        'From bespoke kitchens and wardrobes to striking facades and commercial '
        'fit-outs — we design and build every detail, end to end.'
    ),
    'primary_button_text': 'Explore Our Work',
    'secondary_button_text': 'Get a Quote',
}

# SEO copy, section 3.12 — Contact. Details match Section 1 (Google Business Profile).
CONTACT = {
    'section_label': 'Contact',
    'heading': 'Looking for Interior Designers Near You?',
    'subheading': 'Let’s Create Your Ideal Space',
    'intro': 'Planning a home, modular kitchen, bedroom, office or commercial space? Connect with Us.',
    'description': 'Share a few details and our team will get back within one working day.',
    'address': 'No 5, Ganesh Nagar, Ayapakkam, Chennai 600077',
    'name_placeholder': 'Your Name',
    'phone_placeholder': 'Phone Number',
    'email_placeholder': 'Email Address',
    'service_placeholder': 'Select Interior Design Service',
    'message_placeholder': 'Tell us about your space, room type, size and budget',
    'form_button_text': 'Send Enquiry',
    'success_message': (
        'Thank you for your enquiry. Our interior design team will contact you within one working day.'
    ),
}
OLD_CONTACT = {
    'section_label': 'Contact',
    'heading': 'Tell us about your space',
    'subheading': '',
    'intro': '',
    'description': 'Share a few details and our team will get back within one working day.',
    'address': 'No 5, Ganesh nagar, ayapakkam, Chennai 600077',
    'name_placeholder': 'Name',
    'phone_placeholder': 'Phone',
    'email_placeholder': 'Email',
    'service_placeholder': 'Service Required',
    'message_placeholder': 'Message',
    'form_button_text': 'Send Enquiry',
    'success_message': 'Thank you! Our team will get back to you within one working day.',
}
CONTACT_DETAILS = {
    'phone_numbers': '6374851724, 8525896731',
    'email': 'classiccomfortinteriorexterior@gmail.com',
    'instagram_handle': 'classic_Comfort_interior',
}

# "Service Required" dropdown, in the doc's order ("Other" is always added last by the form)
ENQUIRY_SERVICES = [
    'Modular Kitchen', 'Wardrobe Design', 'TV Unit Design', 'Puja Unit Design', 'False Ceiling',
    'Wall Panelling', 'Bedroom Interior Design', 'Living Room Interior Design', 'Wallpaper Installation',
    'Flooring', 'Office Interior Design', 'Commercial Fit-Out', 'House Elevation Design',
    'ACP Wall Cladding', 'Other',
]

# SEO copy, section 4 — FAQ block (shown after Contact).
FAQ = {'section_label': 'FAQ', 'heading': 'Frequently Asked Questions'}
FAQ_ITEMS = [
    ('What interior design services do you offer?',
     'We provide interior design services for homes and commercial spaces, including modular kitchens, '
     'wardrobes, TV units, false ceilings, wall panelling, flooring and wallpaper installation.'),
    ('Do you handle office interior design?',
     'Yes. We plan and execute office interior design and commercial fit-outs, from layout to final finishing.'),
    ('Can you design both interior and exterior?',
     'Yes. Along with interiors, we do house elevation design, facade cladding and ACP wall cladding.'),
    ('How do I get a quote for my interior works?',
     'Share your space details through the enquiry form or call us. After understanding your requirements, '
     'we prepare a scope and quote.'),
    ('Do you take single-room projects?',
     'Yes. You can book a single kitchen, wardrobe or bedroom, or plan the entire home.'),
]

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


def refresh_copy(obj, new, old):
    """Swap in new copy where a field is blank or still holds the old seeded text.
    Anything typed in admin is kept."""
    changed = False
    for field, value in new.items():
        current = getattr(obj, field).replace('\r\n', '\n')  # admin forms save Windows line breaks
        if current != value and current in ('', old[field]):
            setattr(obj, field, value)
            changed = True
    if changed:
        obj.save()


class Command(BaseCommand):
    help = 'Fill the database with the default website content. Existing content is never overwritten.'

    def handle(self, *args, **options):
        refresh_copy(SiteSettings.load(), SITE_SEO, OLD_SITE_SEO)
        refresh_copy(HeroSection.load(), HERO, OLD_HERO)
        refresh_copy(CTASection.load(), CTA, OLD_CTA)
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
        refresh_copy(about, ABOUT, OLD_ABOUT)
        for title, old_sub, new_sub in ABOUT_WORK_TYPE_RENAMES:
            about.work_types.filter(title=title, subtitle=old_sub).update(subtitle=new_sub)
        for old_text, new_text in ABOUT_PROMISE_RENAMES:
            about.promises.filter(text=old_text).update(text=new_text)
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
        refresh_copy(interior, INTERIOR, OLD_INTERIOR)
        for (old_title, old_desc), (title, description) in zip(OLD_INTERIOR_SERVICES, INTERIOR_SERVICES):
            interior.services.filter(title=old_title, description=old_desc).update(
                title=title, description=description,
            )

        gallery, created = InteriorProjectSection.objects.get_or_create(pk=1, defaults=INTERIOR_GALLERY)
        refresh_copy(gallery, INTERIOR_GALLERY, OLD_INTERIOR_GALLERY)
        if created or not gallery.projects.exists():
            for order, (title, size) in enumerate(INTERIOR_PROJECTS, start=1):
                InteriorProject.objects.create(section=gallery, title=title, size=size, display_order=order)

        exterior, created = ExteriorSection.objects.get_or_create(pk=1, defaults=EXTERIOR)
        if created or not exterior.services.exists():
            for order, (title, description) in enumerate(EXTERIOR_SERVICES, start=1):
                ExteriorService.objects.create(
                    section=exterior, title=title, description=description, display_order=order,
                )
        refresh_copy(exterior, EXTERIOR, OLD_EXTERIOR)
        for (old_title, old_desc), (title, description) in zip(OLD_EXTERIOR_SERVICES, EXTERIOR_SERVICES):
            exterior.services.filter(title=old_title, description=old_desc).update(
                title=title, description=description,
            )

        why, created = WhyChooseSection.objects.get_or_create(pk=1, defaults=WHY_CHOOSE)
        if created or not why.items.exists():
            for order, (title, description) in enumerate(WHY_CHOOSE_ITEMS, start=1):
                WhyChooseItem.objects.create(section=why, title=title, description=description, display_order=order)
        refresh_copy(why, WHY_CHOOSE, OLD_WHY_CHOOSE)
        renamed = 0
        for (old_title, old_desc), (title, description) in zip(OLD_WHY_CHOOSE_ITEMS, WHY_CHOOSE_ITEMS):
            renamed += why.items.filter(title=old_title, description=old_desc).update(
                title=title, description=description,
            )
        if renamed == len(OLD_WHY_CHOOSE_ITEMS):  # old seeded set untouched by admin: add the new points
            for order, (title, description) in enumerate(WHY_CHOOSE_ITEMS, start=1):
                if order > renamed:
                    WhyChooseItem.objects.create(
                        section=why, title=title, description=description, display_order=order,
                    )

        process, created = ProcessSection.objects.get_or_create(pk=1, defaults=PROCESS)
        if created or not process.steps.exists():
            for order, (title, description) in enumerate(PROCESS_STEPS, start=1):
                ProcessStep.objects.create(section=process, title=title, description=description, display_order=order)
        refresh_copy(process, PROCESS, OLD_PROCESS)
        renamed = 0
        for (old_title, old_desc), (title, description) in zip(OLD_PROCESS_STEPS, PROCESS_STEPS):
            renamed += process.steps.filter(title=old_title, description=old_desc).update(
                title=title, description=description,
            )
        if renamed == len(OLD_PROCESS_STEPS):  # old seeded set untouched by admin: add the new steps
            for order, (title, description) in enumerate(PROCESS_STEPS, start=1):
                if order > renamed:
                    ProcessStep.objects.create(
                        section=process, title=title, description=description, display_order=order,
                    )

        portfolio, created = PortfolioSection.objects.get_or_create(pk=1, defaults=PORTFOLIO)
        if created or not portfolio.categories.exists():
            for order, name in enumerate(PROJECT_CATEGORIES, start=1):
                ProjectCategory.objects.create(section=portfolio, name=name, display_order=order)
        refresh_copy(portfolio, PORTFOLIO, OLD_PORTFOLIO)
        for name, hover_title in PROJECT_CATEGORY_TITLES.items():
            portfolio.categories.filter(name=name, hover_title='').update(hover_title=hover_title)
        if not PortfolioProject.objects.exists():
            categories = {c.name: c for c in portfolio.categories.all()}
            for order, (category, title, subtitle, description) in enumerate(PORTFOLIO_PROJECTS, start=1):
                PortfolioProject.objects.create(
                    category=categories[category], title=title, subtitle=subtitle,
                    description=description, display_order=order,
                )
        for old_title, (title, description) in PORTFOLIO_CAPTIONS.items():
            PortfolioProject.objects.filter(title=old_title, description='').update(
                title=title, description=description,
            )

        reviews, created = TestimonialSection.objects.get_or_create(pk=1, defaults=TESTIMONIAL_SECTION)
        refresh_copy(reviews, TESTIMONIAL_SECTION, OLD_TESTIMONIAL_SECTION)
        if created or not reviews.testimonials.exists():
            for order, (quote, client_name, project_type) in enumerate(TESTIMONIALS, start=1):
                Testimonial.objects.create(
                    section=reviews, quote=quote, client_name=client_name,
                    project_type=project_type, display_order=order,
                )

        contact, created = ContactSection.objects.get_or_create(pk=1, defaults={**CONTACT, **CONTACT_DETAILS})
        refresh_copy(contact, CONTACT, OLD_CONTACT)
        if not contact.services.exists():
            for order, name in enumerate(ENQUIRY_SERVICES, start=1):
                EnquiryService.objects.create(contact=contact, name=name, display_order=order)

        faq, created = FAQSection.objects.get_or_create(pk=1, defaults=FAQ)
        if created or not faq.items.exists():
            for order, (question, answer) in enumerate(FAQ_ITEMS, start=1):
                FAQItem.objects.create(section=faq, question=question, answer=answer, display_order=order)

        footer, created = FooterSettings.objects.get_or_create(pk=1)
        if created or not footer.social_links.exists():
            for order, (platform, url) in enumerate(SOCIAL_LINKS, start=1):
                SocialLink.objects.create(footer=footer, platform=platform, url=url, display_order=order)

        self.stdout.write(self.style.SUCCESS('Seed data created. Upload images from the admin panel.'))
