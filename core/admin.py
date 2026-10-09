from django import forms
from django.contrib import admin, messages
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import path, reverse
from django.utils.html import format_html

from .models import (
    AboutPromise, AboutSection, AboutWorkType, ContactSection, CTASection, EmailSettings, Enquiry, EnquiryService, FAQItem, FAQSection, FloatingButtons, FooterSettings, ExteriorSection, ExteriorService,
    HeroSection, InteriorProject,
    InteriorProjectSection, InteriorSection, InteriorService, NavMenuItem, PortfolioProject,
    PortfolioProjectImage, PortfolioSection, ProcessSection, ProcessStep, ProjectCategory, SiteSettings,
    SocialLink, Testimonial, TestimonialSection, WhyChooseItem, WhyChooseSection,
)

admin.site.site_header = 'Classic Comfort — Website Admin'
admin.site.site_title = 'Classic Comfort Admin'
admin.site.index_title = 'Manage your website content'


# ------------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------------
def image_preview(image, height=80):
    if image:
        return format_html('<img src="{}" style="height:{}px;border-radius:4px;" />', image.url, height)
    return '—'


class SingletonAdmin(admin.ModelAdmin):
    """Admin for one-row models: no add/delete, list page goes straight to the edit form."""

    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = self.model.load()
        opts = self.model._meta
        return redirect(reverse(f'admin:{opts.app_label}_{opts.model_name}_change', args=[obj.pk]))


# ------------------------------------------------------------------
# WEBSITE SETTINGS
# ------------------------------------------------------------------
@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonAdmin):
    fieldsets = (
        ('Brand', {'fields': ('site_name', 'logo', 'logo_preview', 'nav_button_text')}),
        ('SEO — Google search', {'fields': (
            'meta_title', 'meta_description', 'meta_keywords', 'meta_author',
            'canonical_url', 'allow_search_engines',
        )}),
        ('Social sharing preview', {
            'fields': ('og_title', 'og_description', 'og_image', 'og_image_preview'),
            'description': 'How the link looks when shared on WhatsApp, Facebook, LinkedIn, etc.',
        }),
        ('Google tools', {'fields': ('google_site_verification', 'google_analytics_id'),
                          'classes': ('collapse',)}),
    )
    readonly_fields = ('logo_preview', 'og_image_preview')

    @admin.display(description='Current logo')
    def logo_preview(self, obj):
        return image_preview(obj.logo)

    @admin.display(description='Current share image')
    def og_image_preview(self, obj):
        return image_preview(obj.og_image, height=120)


# ------------------------------------------------------------------
# NAVBAR MENU
# ------------------------------------------------------------------
@admin.register(NavMenuItem)
class NavMenuItemAdmin(admin.ModelAdmin):
    list_display = ('label', 'section', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    list_display_links = ('label',)


# ------------------------------------------------------------------
# HERO
# ------------------------------------------------------------------
@admin.register(HeroSection)
class HeroSectionAdmin(SingletonAdmin):
    fieldsets = (
        ('Text', {'fields': ('tagline', 'heading', 'description')}),
        ('Background', {'fields': ('background_image', 'background_preview')}),
        ('Buttons', {'fields': ('primary_button_text', 'secondary_button_text')}),
    )
    readonly_fields = ('background_preview',)

    @admin.display(description='Current image')
    def background_preview(self, obj):
        return image_preview(obj.background_image, height=160)


# ------------------------------------------------------------------
# ABOUT US
# ------------------------------------------------------------------
class AboutWorkTypeInline(admin.TabularInline):
    model = AboutWorkType
    fields = ('title', 'subtitle', 'section', 'display_order', 'is_active')
    extra = 0


class AboutPromiseInline(admin.TabularInline):
    model = AboutPromise
    fields = ('text', 'display_order', 'is_active')
    extra = 0


@admin.register(AboutSection)
class AboutSectionAdmin(SingletonAdmin):
    fieldsets = (
        ('Text', {'fields': ('section_label', 'heading', 'intro', 'content', 'closing_text')}),
        ('Image', {'fields': ('image', 'image_preview')}),
        ('Mission', {'fields': ('mission_title', 'mission_text')}),
        ('Vision', {'fields': ('vision_title', 'vision_text')}),
        ('Promise', {'fields': ('promise_title',),
                     'description': 'Add the promise words in the table at the bottom of this page.'}),
    )
    readonly_fields = ('image_preview',)
    inlines = (AboutWorkTypeInline, AboutPromiseInline)

    @admin.display(description='Current image')
    def image_preview(self, obj):
        return image_preview(obj.image, height=160)


# ------------------------------------------------------------------
# SERVICE SECTIONS (Interior / Exterior Works)
# ------------------------------------------------------------------
class ServiceItemInline(admin.StackedInline):
    fields = (('title', 'display_order', 'is_active'), 'description', ('image', 'image_preview'))
    readonly_fields = ('image_preview',)
    extra = 0

    @admin.display(description='Current image')
    def image_preview(self, obj):
        return image_preview(obj.image)


class ServiceSectionAdmin(SingletonAdmin):
    fields = ('section_label', 'heading', 'description', 'enquire_button_text')


class InteriorServiceInline(ServiceItemInline):
    model = InteriorService


@admin.register(InteriorSection)
class InteriorSectionAdmin(ServiceSectionAdmin):
    inlines = (InteriorServiceInline,)


class ExteriorServiceInline(ServiceItemInline):
    model = ExteriorService


@admin.register(ExteriorSection)
class ExteriorSectionAdmin(ServiceSectionAdmin):
    inlines = (ExteriorServiceInline,)


# ------------------------------------------------------------------
# PROJECT GALLERIES (Interior / Exterior Projects)
# ------------------------------------------------------------------
class ProjectItemInline(admin.TabularInline):
    fields = ('display_order', 'title', 'size', 'image', 'image_preview', 'is_active')
    readonly_fields = ('image_preview',)
    extra = 0

    @admin.display(description='Preview')
    def image_preview(self, obj):
        return image_preview(obj.image, height=60)


class ProjectSectionAdmin(SingletonAdmin):
    fields = ('section_label', 'heading', 'description')


class InteriorProjectInline(ProjectItemInline):
    model = InteriorProject


@admin.register(InteriorProjectSection)
class InteriorProjectSectionAdmin(ProjectSectionAdmin):
    inlines = (InteriorProjectInline,)


# ------------------------------------------------------------------
# NUMBERED LISTS (Why Choose Us / Our Process)
# ------------------------------------------------------------------
class NumberedItemInline(admin.TabularInline):
    fields = ('display_order', 'title', 'description', 'is_active')
    extra = 0


class NumberedSectionAdmin(SingletonAdmin):
    fields = ('section_label', 'heading')


class WhyChooseItemInline(NumberedItemInline):
    model = WhyChooseItem


@admin.register(WhyChooseSection)
class WhyChooseSectionAdmin(NumberedSectionAdmin):
    inlines = (WhyChooseItemInline,)


class ProcessStepInline(NumberedItemInline):
    model = ProcessStep


@admin.register(ProcessSection)
class ProcessSectionAdmin(NumberedSectionAdmin):
    inlines = (ProcessStepInline,)


# ------------------------------------------------------------------
# PORTFOLIO (Our Projects)
# ------------------------------------------------------------------
class ProjectCategoryInline(admin.TabularInline):
    model = ProjectCategory
    fields = ('name', 'hover_title', 'display_order', 'is_active')
    extra = 0


@admin.register(PortfolioSection)
class PortfolioSectionAdmin(SingletonAdmin):
    fields = ('section_label', 'heading', 'description', 'all_filter_text', 'all_filter_title')
    inlines = (ProjectCategoryInline,)


class PortfolioProjectImageInline(admin.TabularInline):
    model = PortfolioProjectImage
    fields = ('image', 'image_preview', 'caption', 'display_order', 'is_active')
    readonly_fields = ('image_preview',)
    extra = 1

    @admin.display(description='Preview')
    def image_preview(self, obj):
        return image_preview(obj.image, height=60)


@admin.register(PortfolioProject)
class PortfolioProjectAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'title', 'category', 'subtitle', 'photo_count', 'display_order', 'is_active')
    list_display_links = ('thumbnail', 'title')
    list_editable = ('display_order', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'subtitle')
    fields = ('category', 'title', 'subtitle', 'description', 'image', 'image_preview', 'display_order', 'is_active')
    readonly_fields = ('image_preview',)
    inlines = (PortfolioProjectImageInline,)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category').prefetch_related('images')

    @admin.display(description='Image')
    def thumbnail(self, obj):
        return image_preview(obj.image, height=50)

    @admin.display(description='Cover image')
    def image_preview(self, obj):
        return image_preview(obj.image, height=160)

    @admin.display(description='Extra photos')
    def photo_count(self, obj):
        return len(obj.images.all())


# ------------------------------------------------------------------
# TESTIMONIALS
# ------------------------------------------------------------------
class TestimonialInline(admin.StackedInline):
    model = Testimonial
    fields = ('quote', ('client_name', 'project_type'), ('display_order', 'is_active'))
    extra = 0


@admin.register(TestimonialSection)
class TestimonialSectionAdmin(SingletonAdmin):
    fields = ('section_label', 'heading', 'description')
    inlines = (TestimonialInline,)


# ------------------------------------------------------------------
# START TODAY BANNER
# ------------------------------------------------------------------
@admin.register(CTASection)
class CTASectionAdmin(SingletonAdmin):
    fieldsets = (
        ('Text', {'fields': ('section_label', 'heading', 'description')}),
        ('Background', {'fields': ('background_image', 'background_preview')}),
        ('Buttons', {'fields': ('primary_button_text', 'secondary_button_text')}),
    )
    readonly_fields = ('background_preview',)

    @admin.display(description='Current image')
    def background_preview(self, obj):
        return image_preview(obj.background_image, height=160)


# ------------------------------------------------------------------
# CONTACT + ENQUIRIES
# ------------------------------------------------------------------
class EnquiryServiceInline(admin.TabularInline):
    model = EnquiryService
    fields = ('name', 'display_order', 'is_active')
    extra = 0


@admin.register(ContactSection)
class ContactSectionAdmin(SingletonAdmin):
    fieldsets = (
        ('Text', {'fields': ('section_label', 'heading', 'subheading', 'intro', 'description')}),
        ('Contact details', {'fields': ('address', 'phone_numbers', 'email', 'instagram_handle')}),
        ('Enquiry form', {
            'fields': ('name_placeholder', 'phone_placeholder', 'email_placeholder', 'service_placeholder',
                       'message_placeholder', 'form_button_text', 'success_message'),
            'description': 'The service dropdown uses the options in the table at the bottom of this page '
                           '("Other" is always added). If that table is empty, it is filled from the '
                           'Interior and Exterior service cards.',
        }),
    )
    inlines = (EnquiryServiceInline,)


# ------------------------------------------------------------------
# FAQ
# ------------------------------------------------------------------
class FAQItemInline(admin.StackedInline):
    model = FAQItem
    fields = ('question', 'answer', 'display_order', 'is_active')
    extra = 0


@admin.register(FAQSection)
class FAQSectionAdmin(SingletonAdmin):
    fields = ('section_label', 'heading')
    inlines = (FAQItemInline,)


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'name', 'phone_link', 'email', 'service', 'status', 'email_sent')
    list_display_links = ('created_at', 'name')
    list_editable = ('status',)
    list_filter = ('status', 'service', 'created_at')
    search_fields = ('name', 'phone', 'email', 'message')
    readonly_fields = ('name', 'phone', 'email', 'service', 'message', 'created_at', 'email_sent', 'ip_address')
    fieldsets = (
        ('Enquiry', {'fields': ('created_at', 'name', 'phone', 'email', 'service', 'message')}),
        ('Follow-up', {'fields': ('status', 'notes')}),
        ('Technical', {'fields': ('email_sent', 'ip_address'), 'classes': ('collapse',)}),
    )
    actions = ('mark_contacted', 'mark_closed')

    def has_add_permission(self, request):
        return False  # enquiries only come from the website form

    @admin.display(description='Phone')
    def phone_link(self, obj):
        return format_html('<a href="tel:+91{}">{}</a>', obj.phone, obj.phone)

    @admin.action(description='Mark selected as Contacted')
    def mark_contacted(self, request, queryset):
        queryset.update(status=Enquiry.STATUS_CONTACTED)

    @admin.action(description='Mark selected as Closed')
    def mark_closed(self, request, queryset):
        queryset.update(status=Enquiry.STATUS_CLOSED)


# ------------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------------
class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    fields = ('platform', 'url', 'display_order', 'is_active')
    extra = 0


@admin.register(FooterSettings)
class FooterSettingsAdmin(SingletonAdmin):
    fieldsets = (
        ('Logo & description', {
            'fields': ('footer_logo', 'logo_preview', 'about_text', 'follow_text'),
        }),
        ('Column headings', {
            'fields': ('quick_links_title', 'interior_title', 'exterior_title', 'contact_title'),
            'description': 'The links under each heading are filled automatically from the other sections.',
        }),
        ('Bottom bar', {'fields': ('copyright_text', 'credit_prefix', 'credit_name', 'credit_url')}),
    )
    readonly_fields = ('logo_preview',)
    inlines = (SocialLinkInline,)

    @admin.display(description='Logo shown in footer')
    def logo_preview(self, obj):
        logo = obj.footer_logo or SiteSettings.load().logo
        return image_preview(logo)


# ------------------------------------------------------------------
# FLOATING CONTACT BUTTONS
# ------------------------------------------------------------------
@admin.register(FloatingButtons)
class FloatingButtonsAdmin(SingletonAdmin):
    fieldsets = (
        ('Call', {'fields': ('show_call', 'call_number')}),
        ('WhatsApp', {'fields': ('show_whatsapp', 'whatsapp_number', 'whatsapp_message')}),
        ('Instagram', {'fields': ('show_instagram', 'instagram_url')}),
    )


# ------------------------------------------------------------------
# EMAIL / SMTP
# ------------------------------------------------------------------
class EmailSettingsForm(forms.ModelForm):
    smtp_password = forms.CharField(
        label='Email password / App password',
        required=False,
        widget=forms.PasswordInput(render_value=False),
        help_text='Leave blank to keep the current password.',
    )

    class Meta:
        model = EmailSettings
        fields = '__all__'

    def clean_smtp_password(self):
        value = self.cleaned_data.get('smtp_password')
        if not value and self.instance.pk:
            return self.instance.smtp_password  # keep existing
        return value


@admin.register(EmailSettings)
class EmailSettingsAdmin(SingletonAdmin):
    form = EmailSettingsForm
    change_form_template = 'admin/core/emailsettings/change_form.html'
    fieldsets = (
        ('SMTP server', {'fields': ('smtp_host', 'smtp_port', 'use_tls', 'use_ssl')}),
        ('Login', {'fields': ('smtp_username', 'smtp_password')}),
        ('Addresses', {'fields': ('from_email', 'notify_email')}),
        ('Confirmation email to customer', {
            'fields': ('send_auto_reply', 'auto_reply_subject', 'auto_reply_message'),
        }),
    )

    def get_urls(self):
        custom = [
            path('send-test/', self.admin_site.admin_view(self.send_test_email),
                 name='core_emailsettings_send_test'),
        ]
        return custom + super().get_urls()

    def send_test_email(self, request):
        cfg = EmailSettings.load()
        target = reverse('admin:core_emailsettings_change', args=[cfg.pk])
        if not cfg.is_configured or not cfg.notify_email:
            messages.error(request, 'Please fill in the SMTP server, login, password and "Send enquiries to" first.')
            return redirect(target)
        try:
            send_mail(
                'Test email from your website',
                'Your email settings are working correctly.',
                cfg.from_email or cfg.smtp_username,
                [cfg.notify_email],
            )
            messages.success(request, f'Test email sent to {cfg.notify_email}.')
        except Exception as exc:
            messages.error(request, f'Could not send email: {exc}')
        return redirect(target)


# ------------------------------------------------------------------
# ORDER MODELS IN THE ADMIN SIDEBAR (page order, not alphabetical)
# ------------------------------------------------------------------
ADMIN_MODEL_ORDER = [
    'SiteSettings',
    'NavMenuItem',
    'HeroSection',
    'AboutSection',
    'InteriorSection',
    'InteriorProjectSection',
    'ExteriorSection',
    'WhyChooseSection',
    'ProcessSection',
    'PortfolioSection',
    'PortfolioProject',
    'TestimonialSection',
    'CTASection',
    'ContactSection',
    'Enquiry',
    'FooterSettings',
    'FloatingButtons',
    # next sections go here...
    'EmailSettings',
]

_original_get_app_list = admin.AdminSite.get_app_list


def _ordered_get_app_list(self, request, app_label=None):
    app_list = _original_get_app_list(self, request, app_label)
    for app in app_list:
        if app['app_label'] == 'core':
            app['models'].sort(
                key=lambda m: ADMIN_MODEL_ORDER.index(m['object_name'])
                if m['object_name'] in ADMIN_MODEL_ORDER else len(ADMIN_MODEL_ORDER)
            )
    return app_list


admin.AdminSite.get_app_list = _ordered_get_app_list
