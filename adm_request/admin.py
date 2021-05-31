from django.contrib import admin
from .models import Document, ADMRequest, StoryRecord, Conclusion, \
    ConclusionType, Investigation, Reason
from django.contrib.admin import site
import adminactions.actions as actions

# register all adminactions
actions.add_to_site(site)


class DocumentAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'name',
                    'file',
                    'created',
                    'updated'
                    ]
    list_filter = ['created',
                   ]
    prepopulated_fields = {'slug': ('file',)}


class ReasonAdmin(admin.ModelAdmin):
    list_display = ['name',
                    'created',
                    'updated',
                    ]
    list_filter = ['created',
                   'updated',
                   ]


class StoryRecordInline(admin.StackedInline):
    model = StoryRecord
    fk_name = 'investigation'
    verbose_name = 'Запись'
    verbose_name_plural = 'История проверки'


class ADMRequestAdmin(admin.ModelAdmin):
    list_display = ['number',
                    'reason',
                    'amount',
                    'date',
                    ]
    list_filter = ['date',
                   ]
    prepopulated_fields = {'slug': ('number', 'date')}


class DocumentsInline(admin.TabularInline):
    model = Investigation.documents.through
    verbose_name = 'Документ'
    verbose_name_plural = 'Документы'


class InvestigationAdmin(admin.ModelAdmin):
    list_display = ['adm_request',
                    'description',
                    'result',
                    ]
    list_filter = ['created',
                   'updated',
                   ]
    inlines = [StoryRecordInline,
               DocumentsInline,
               ]
    exclude = ('documents',
               )


class ConclusionTypeAdmin(admin.ModelAdmin):
    list_display = ['name',
                    'description',
                    'created',
                    'updated',
                    ]
    list_filter = ['created',
                   ]


class ConclusionAdmin(admin.ModelAdmin):
    list_display = ['number',
                    'conclusion_type',
                    'created',
                    'updated',
                    'payoff_required',
                    ]
    list_filter = ['conclusion_type',
                   'created',
                   'payoff_required',
                   ]


admin.site.register(Document, DocumentAdmin)
admin.site.register(ADMRequest, ADMRequestAdmin)
admin.site.register(Investigation, InvestigationAdmin)
admin.site.register(ConclusionType, ConclusionTypeAdmin)
admin.site.register(Conclusion, ConclusionAdmin)
admin.site.register(Reason, ReasonAdmin)
