from django.contrib import messages
from django.core.cache import cache
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .emails import send_enquiry_emails
from .forms import EnquiryForm

from .models import (
    AboutSection, ContactSection, CTASection, ExteriorSection, FloatingButtons, FooterSettings, HeroSection, InteriorProjectSection, InteriorSection, NavMenuItem,
    PortfolioProject, PortfolioProjectImage, PortfolioSection,
    ProcessSection, TestimonialSection, WhyChooseSection,
)


def index(request, enquiry_form=None):
    about = AboutSection.load()
    interior = InteriorSection.load()
    interior_gallery = InteriorProjectSection.load()
    exterior = ExteriorSection.load()
    why_choose = WhyChooseSection.load()
    process = ProcessSection.load()
    portfolio = PortfolioSection.load()
    testimonials = TestimonialSection.load()
    contact = ContactSection.load()
    footer = FooterSettings.load()
    context = {
        'nav_items': NavMenuItem.objects.filter(is_active=True),
        'hero': HeroSection.load(),
        'about': about,
        'about_work_types': about.work_types.filter(is_active=True),
        'about_promises': about.promises.filter(is_active=True),
        'interior': interior,
        'interior_services': interior.services.filter(is_active=True),
        'interior_gallery': interior_gallery,
        'interior_projects': interior_gallery.projects.filter(is_active=True),
        'exterior': exterior,
        'exterior_services': exterior.services.filter(is_active=True),
        'why_choose': why_choose,
        'why_choose_items': why_choose.items.filter(is_active=True),
        'process': process,
        'process_steps': process.steps.filter(is_active=True),
        'portfolio': portfolio,
        'portfolio_categories': portfolio.categories.filter(is_active=True),
        'portfolio_projects': (
            PortfolioProject.objects
            .filter(is_active=True, category__is_active=True)
            .select_related('category')
            .prefetch_related(Prefetch('images', queryset=PortfolioProjectImage.objects.filter(is_active=True)))
        ),
        'testimonial_section': testimonials,
        'testimonials': testimonials.testimonials.filter(is_active=True),
        'cta': CTASection.load(),
        'contact': contact,
        'footer': footer,
        'floating': FloatingButtons.load(),
        'footer_social_links': footer.social_links.filter(is_active=True).exclude(url=''),
        'enquiry_form': enquiry_form or EnquiryForm(service_placeholder=contact.service_placeholder),
    }
    return render(request, 'index.html', context)


ENQUIRY_LIMIT = 5            # submissions allowed...
ENQUIRY_WINDOW = 60 * 60     # ...per IP address per hour


@require_POST
def submit_enquiry(request):
    """Contact form endpoint. Returns JSON for fetch() requests, or redirects back for plain posts."""
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    contact = ContactSection.load()
    form = EnquiryForm(request.POST, service_placeholder=contact.service_placeholder)
    ip = request.META.get('REMOTE_ADDR')

    def respond(ok, status=200, errors=None, message=''):
        if is_ajax:
            return JsonResponse({'ok': ok, 'message': message, 'errors': errors or {}}, status=status)
        if ok:
            messages.success(request, message)
            return redirect('/#contact')
        if errors:  # show the page again with the errors next to each field
            return index(request, enquiry_form=form)
        messages.error(request, message)
        return redirect('/#contact')

    # Bots fill the hidden field: pretend success so they don't retry.
    if form.is_spam:
        return respond(True, message=contact.success_message)

    rate_key = f'enquiry-rate:{ip}'
    if cache.get(rate_key, 0) >= ENQUIRY_LIMIT:
        return respond(False, status=429,
                       message='Too many enquiries from your connection. Please try again later or call us.')

    if not form.is_valid():
        errors = {field: [str(e) for e in errs] for field, errs in form.errors.items()}
        return respond(False, status=400, errors=errors, message='Please correct the highlighted fields.')

    enquiry = form.save(commit=False)
    enquiry.ip_address = ip
    enquiry.save()
    cache.set(rate_key, cache.get(rate_key, 0) + 1, ENQUIRY_WINDOW)

    if send_enquiry_emails(enquiry):
        enquiry.email_sent = True
        enquiry.save(update_fields=['email_sent'])

    return respond(True, message=contact.success_message)
