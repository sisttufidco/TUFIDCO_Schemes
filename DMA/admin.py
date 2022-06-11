from django.contrib import admin
from TUFIDCOapp.models import *
from DMA.models import *
from ULBForms.models import *
from django.contrib import admin
from django.db.models import Count, Sum,  Func
from import_export.admin import ImportExportModelAdmin
from django.db.models import Q
from .models import DistrictWiseReport
from .resources import MunicipalityDetailsResource


class MunicipalityDetailsAdmin(ImportExportModelAdmin, admin.AdminSite):
    resource_class = MunicipalityDetailsResource
    exclude = ['user']

    search_fields = [
        'municipality_name',
        'district',
        'region'
    ]
    list_display = [
        'municipality_name',
        'district',
        'region',
        'mc',
        'me',
        'email_id1',
        'date_and_time'
    ]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.date_and_time = datetime.now()
        obj.save()

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': True,
            'show_save_and_add_another': False,
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

    def get_queryset(self, request):
        qs = super(MunicipalityDetailsAdmin, self).get_queryset(request)
        if not request.user.groups.filter(name__in=["Admin", ]).exists():
            return qs.filter(user=request.user)
        return qs

    def has_add_permission(self, request, *args, **kwargs):
        return not MunicipalityDetails.objects.filter(user=request.user).exists() and not request.user.groups.filter(
            name__in=[
                "Admin", "CMD_DGM"]).exists()


admin.site.register(MunicipalityDetails, MunicipalityDetailsAdmin)

@admin.register(MasterReport)
class MasterReportAdmin(admin.ModelAdmin):
    change_list_template = 'admin/DMAPhysicalAndFinancialReport.html'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        final_data = []
        sector_list = list(MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyType__AgencyType='Municipality').filter(Scheme__Scheme="KNMT").distinct())
        for sector in sector_list:
            Schemeshare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(Sector=sector).filter(AgencyType__AgencyType='Municipality').aggregate(SchemeShare=Sum('SchemeShare'))
            ULBshare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector=sector).filter(AgencyType__AgencyType='Municipality').aggregate(ULBShare=Sum('ULBShare'))
            total = Schemeshare['SchemeShare'] + ULBshare['ULBShare']
            approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector=sector).filter(AgencyType__AgencyType='Municipality').count()
            Amountspend = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Municipality').filter(Sector=sector).aggregate(sum=Sum('valueofworkdone'))
            Workorder  = AgencySanctionModel.objects.filter(Scheme='KNMT').filter(ULBType='Municipality').filter(Sector=sector).aggregate(sum=Sum('work_awarded_amount1'))
            completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Municipality').filter(Sector=sector).filter(status='Completed').count()
            Value_work_done_completed  = AgencyProgressModel.objects.filter(Scheme="KNMT").filter(ULBType='Municipality').filter(Sector=sector).filter(status='Completed').aggregate(sum=Sum('valueofworkdone'))
            Value_work_done_inprogress  = AgencyProgressModel.objects.filter(Scheme="KNMT").filter(ULBType='Municipality').filter(Sector=sector).filter(status='In Progress').aggregate(sum=Sum('valueofworkdone'))
            Inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector=sector).filter(ULBType='Municipality').filter(status='In Progress').count()
            Final = list(AgencyProgressModel.objects.values_list('Project_ID', flat=True).filter(ULBType='Municipality').filter(Scheme='KNMT').filter(Sector=sector).filter(status='Not Commenced'))
            TS_awarded = AgencySanctionModel.objects.filter(Scheme='KNMT').filter(Sector=sector).filter(ULBType='Municipality').filter(ts_awarded='Yes').filter(Q(Project_ID__in=Final)).count()
            WO_awarded = AgencySanctionModel.objects.filter(Scheme='KNMT').filter(Sector=sector).filter(ULBType='Municipality').filter(wd_awarded='Yes').filter(Q(Project_ID__in=Final)).count()
            taken = Inprogress + completed
            toBeCommenced = approved - taken
            dic = {
                "Sector":sector,
                "SchemeShare": Schemeshare,
                "ULBShare": ULBshare,
                "Total": total,
                "Approved": approved,
                "amountspend": Amountspend,
                "workorder": Workorder,
                "Completed": completed,
                "value_work_done_completed":Value_work_done_completed,
                "value_work_done_inprogress":Value_work_done_inprogress,
                "inprogress":Inprogress,
                "TS_Awarded":TS_awarded,
                "WO_Awarded":WO_awarded,
                "Taken":taken,
                "ToBeCommenced":toBeCommenced
            }
            final_data.append(dic)

        SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(SchemeShare=Sum('SchemeShare'))
        ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(ULBShare=Sum('ULBShare'))
        ProjectCost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            ProjectCost=Sum('ApprovedProjectCost'))
        work_approved_total = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').count()
        work_amountspend = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Municipality').aggregate(
            sum=Sum('valueofworkdone'))
        workorder_total = AgencySanctionModel.objects.filter(Scheme='KNMT').filter(ULBType='Municipality').aggregate(
            sum=Sum('work_awarded_amount1'))
        works_inprogress_total = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Municipality').filter(status='In Progress').count()
        works_completed_total = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Municipality').filter(status='Completed').count()
        works_taken_total = works_inprogress_total + works_completed_total
        works_ToBeCommenced = work_approved_total-works_taken_total
        Overall_value_work_done_completed  = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Municipality').filter(status='Completed').aggregate(sum=Sum('valueofworkdone'))
        Overall_value_work_done_inprogress  = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Municipality').filter(status='In Progress').aggregate(sum=Sum('valueofworkdone'))
        Overall_final = list(AgencyProgressModel.objects.values_list('Project_ID', flat=True).filter(ULBType='Municipality').filter(Scheme='KNMT').filter(
            status='Not Commenced'))
        Overall_TS_Awarded = AgencySanctionModel.objects.filter(Scheme='KNMT').filter(ULBType='Municipality').filter(ts_awarded='Yes').filter(Q(Project_ID__in=Overall_final)).count()
        Overall_WO_Awarded = AgencySanctionModel.objects.filter(Scheme='KNMT').filter(ULBType='Municipality').filter(wd_awarded='Yes').filter(Q(Project_ID__in=Overall_final)).count()
        extra_context = {
            'Overall_value_work_done_completed':Overall_value_work_done_completed,
            'Overall_value_work_done_inprogress':Overall_value_work_done_inprogress,
            'Overall_TS_Awarded':Overall_TS_Awarded,
            'Overall_WO_Awarded':Overall_WO_Awarded,
            'works_ToBeCommenced':works_ToBeCommenced,
            'work_amountspend':work_amountspend,
            'workorder_total':workorder_total,   
            'works_taken_total': works_taken_total,
            'works_inprogress_total': works_inprogress_total,
            'works_completed_total': works_completed_total,
            'work_approved_total': work_approved_total,
            'ProjectCost': ProjectCost,
            'ULBShare': ULBShare,
            'SchemeShare': SchemeShare,
            'final_data':final_data,
        }
        response.context_data.update(extra_context)
        return response


class Round(Func):
    function = "ROUND"
    template = "%(function)s(%(expressions)s::numeric, 2)"


@admin.register(DistrictWiseReport)
class DistrictWiseReportAdmin(admin.ModelAdmin):
    change_list_template = "admin/districtwisereport.html"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
            'Project_ID': Count('Project_ID'),
            'ApprovedCost': Sum('ApprovedProjectCost'),
        }

        response.context_data['report_total'] = dict(
            qs.aggregate(**metrics)
        )

        final_data = []
        district_list = list(MasterSanctionForm.objects.values_list('District__District', flat=True).order_by('District__District').filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType="Municipality").all().distinct())
    
        for district in district_list:
            BTRoadNo = MasterSanctionForm.objects.filter(Sector='BT Road').filter(District__District=district).filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').count()
            BTRoadCost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(District__District=district).filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
            CCRoadNo = MasterSanctionForm.objects.filter(Sector='CC Road').filter(District__District=district).filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').count()
            CCRoadCost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(District__District=district).filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
            CrematoriumNo = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(District__District=district).filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').count()
            CrematoriumCost =  MasterSanctionForm.objects.filter(Sector='Crematorium').filter(District__District=district).filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
            CulvertNo =MasterSanctionForm.objects.filter(Sector='Culvert').filter(District__District=district).filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').count()
            CulvertCost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(District__District=district).filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
            KC_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(District__District=district).filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').count()
            KC_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(District__District=district).filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
            MarketNo = MasterSanctionForm.objects.filter(Sector='Market').filter(District__District=district).filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').count()
            MarketCost = MasterSanctionForm.objects.filter(Sector='Market').filter(District__District=district).filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
            ParksNo = MasterSanctionForm.objects.filter(Sector='Parks').filter(District__District=district).filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').count()
            ParksCost = MasterSanctionForm.objects.filter(Sector='Parks').filter(District__District=district).filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
            PBno = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(District__District=district).filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').count()
            PBCost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(District__District=district).filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
            SWDno = MasterSanctionForm.objects.filter(Sector='SWD').filter(District__District=district).filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').count()
            SWDCost = MasterSanctionForm.objects.filter(Sector='SWD').filter(District__District=district).filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
            WBno = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(District__District=district).filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').count()
            WBCost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(District__District=district).filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
            totalno = MasterSanctionForm.objects.filter(District__District=district).filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').count()
            totalcost = MasterSanctionForm.objects.filter(District__District=district).filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
            
            dic = {
                "district": district,
                "BTRoadNo": BTRoadNo,
                "BTRoadCost": BTRoadCost,
                "CCRoadNo": CCRoadNo,
                "CCRoadCost": CCRoadCost,
                "CrematoriumNo": CrematoriumNo,
                "CrematoriumCost": CrematoriumCost,
                "CulvertNo": CulvertNo,
                "CulvertCost": CulvertCost,
                "KC_No": KC_No,
                "KC_Cost": KC_Cost,
                "MarketNo": MarketNo,
                "MarketCost": MarketCost,
                "ParksNo": ParksNo,
                "ParksCost": ParksCost,
                "PBno": PBno,
                "PBCost": PBCost,
                "SWDno": SWDno,
                "SWDCost": SWDCost,
                "WBno": WBno,
                "WBCost": WBCost,
                "totalno": totalno,
                "totalcost": totalcost,
            }
            final_data.append(dic)

        DMA_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').count()
        DMA_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        DMA_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').count()
        DMA_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        DMA_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').count()
        DMA_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        DMA_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter( Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').count()
        DMA_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert ').filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        DMA_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').count()
        DMA_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        DMA_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').count()
        DMA_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        DMA_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').count()
        DMA_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        DMA_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').count()
        DMA_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        DMA_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').count()
        DMA_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        DMA_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').count()
        DMA_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        DMA_total_no = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').count()
        DMA_total_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        
        extra_context = {
            "final_data": final_data,
            'DMA_BT_RoadDMA_No': DMA_BT_RoadDMA_No,
            'DMA_BT_RoadDMA_Cost': DMA_BT_RoadDMA_Cost,
            'DMA_CC_RoadDMA_No': DMA_CC_RoadDMA_No,
            'DMA_CC_RoadDMA_Cost': DMA_CC_RoadDMA_Cost,
            'DMA_CrematoriumDMA_Cost': DMA_CrematoriumDMA_Cost,
            'DMA_CrematoriumDMA_No': DMA_CrematoriumDMA_No,
            'DMA_CulvertDMA_Cost': DMA_CulvertDMA_Cost,
            'DMA_CulvertDMA_No': DMA_CulvertDMA_No,
            'DMA_KnowledgeDMA_Centre_No': DMA_KnowledgeDMA_Centre_No,
            'DMA_KnowledgeDMA_Centre_Cost': DMA_KnowledgeDMA_Centre_Cost,
            'DMA_MarketDMA_No': DMA_MarketDMA_No,
            'DMA_MarketDMA_Cost': DMA_MarketDMA_Cost,
            'DMA_ParksDMA_No': DMA_ParksDMA_No,
            'DMA_ParksDMA_Cost': DMA_ParksDMA_Cost,
            'DMA_PaverBlockDMA_No': DMA_PaverBlockDMA_No,
            'DMA_PaverBlockDMA_Cost': DMA_PaverBlockDMA_Cost,
            'DMA_SWDDMA_No': DMA_SWDDMA_No,
            'DMA_SWDDMA_Cost': DMA_SWDDMA_Cost,
            'DMA_WBDMA_No': DMA_WBDMA_No,
            'DMA_WBDMA_Cost': DMA_WBDMA_Cost,
            'DMA_total_no': DMA_total_no,
            'DMA_total_cost': DMA_total_cost,
        }
        response.context_data.update(extra_context)
        response.context_data['KNMT_Sector'] = list(qs.values('Sector').filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').annotate(**metrics).order_by('Sector'))
        return response



