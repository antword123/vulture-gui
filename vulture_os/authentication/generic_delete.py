#!/home/vlt-os/env/bin/python
"""This file is part of Vulture OS.

Vulture OS is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Vulture OS is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Vulture OS.  If not, see http://www.gnu.org/licenses/.
"""
__author__ = "Kevin GUILLEMOT"
__credits__ = []
__license__ = "GPLv3"
__version__ = "4.0.0"
__maintainer__ = "Vulture OS"
__email__ = "contact@vultureproject.org"
__doc__ = 'Classes used to delete objects'

# Django system imports
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View

# Django project imports
from authentication.kerberos.models import KerberosRepository
from authentication.ldap.models import LDAPRepository
from authentication.learning_profiles.models import LearningProfile
from authentication.openid.models import OpenIDRepository
from authentication.otp.models import OTPRepository
from authentication.radius.models import RadiusRepository
from authentication.user_portal.models import UserAuthentication
from authentication.auth_access_control.models import AuthAccessControl
from authentication.portal_template.models import PortalTemplate, TemplateImage
from authentication.totp_profiles.models import TOTPProfile
from authentication.user_scope.models import UserScope
from workflow.models import Workflow

# Required exceptions imports
from django.core.exceptions import ObjectDoesNotExist

# Logger configuration imports
import logging
logging.config.dictConfig(settings.LOG_SETTINGS)
logger = logging.getLogger('gui')


# Do NOT instantiate directly - it's an abstract class
# Create a child class and instantiate-it
# Do not forget used_by mandatory method in all childs
class DeleteView(View):
    template_name = 'generic_delete.html'
    menu_name = _("")
    obj = None
    redirect_url = ""
    delete_url = ""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DeleteView, self).dispatch(*args, **kwargs)

    def get(self, request, object_id, **kwargs):
        try:
            obj_inst = self.obj.objects.get(pk=object_id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound('Object not found.')

        used_by = self.used_by(obj_inst)

        return render(request, self.template_name, {
            'object_id': object_id,
            'menu_name': self.menu_name,
            'delete_url': self.delete_url,
            'redirect_url': self.redirect_url,
            'obj_inst': obj_inst,
            'used_by': used_by
        })

    def post(self, request, object_id, **kwargs):
        if hasattr(request, "JSON"):
            confirm = request.JSON.get('confirm')
        else:
            confirm = request.POST.get('confirm')

        if confirm == 'yes':
            try:
                obj_inst = self.obj.objects.get(pk=object_id)
            except ObjectDoesNotExist:
                return HttpResponseNotFound('Object not found.')
            obj_inst.delete()
        
        if kwargs.get('api'):
            return JsonResponse({"status": True})
        return HttpResponseRedirect(self.redirect_url)

    def used_by(self, objet):
        """ Retrieve all objects that use the current object
        Return a list of strings, printed in template as "Used by this object:"
        """
        # return [str(i) for i in objet.]
        return []


class DeleteOTPRepository(DeleteView):
    menu_name = _("Authentication -> OTP -> Delete")
    obj = OTPRepository
    redirect_url = "/authentication/otp/"
    delete_url = "/authentication/otp/delete/"

    # get, post and used_by methods herited from mother class

    #def used_by(self, objet):
    #    return [str(i) for i in objet.user_authentication_set.all()]


class DeleteLDAPRepository(DeleteView):
    menu_name = _("Authentication -> LDAP -> Delete")
    obj = LDAPRepository
    redirect_url = "/authentication/ldap/"
    delete_url = "/authentication/ldap/delete/"

    def used_by(self, object):
        return ["Portal " + w.name for w in UserAuthentication.objects.filter(repositories=object)]

    # get, post and used_by methods herited from mother class


class DeleteKerberosRepository(DeleteView):
    menu_name = _("Authentication -> Kerberos -> Delete")
    obj = KerberosRepository
    redirect_url = "/authentication/kerberos/"
    delete_url = "/authentication/kerberos/delete/"

    # get, post and used_by methods herited from mother class


class DeleteRadiusRepository(DeleteView):
    menu_name = _("Authentication -> Radius -> Delete")
    obj = RadiusRepository
    redirect_url = "/authentication/radius/"
    delete_url = "/authentication/radius/delete/"

    # get, post and used_by methods herited from mother class


class DeleteUserAuthentication(DeleteView):
    menu_name = _("Authentication Portal -> User authentication -> Delete")
    obj = UserAuthentication
    redirect_url = "/portal/user_authentication/"
    delete_url = "/portal/user_authentication/delete/"

    def used_by(self, object):
        linked_objects = ["Workflow " + w.name for w in Workflow.objects.filter(authentication=object)]
        if object.enable_external:
            try:
                linked_connector = OpenIDRepository.objects.get(client_id=object.oauth_client_id,
                                                            client_secret=object.oauth_client_secret,
                                                            provider="openid")
                linked_objects += ["Portal " + portal.name for portal in UserAuthentication.objects.filter(repositories=linked_connector)]
            except OpenIDRepository.DoesNotExist:
                logger.warning(f"Did not find linked connector while deleting IDP portal {object.name}")
        return linked_objects

    def post(self, request, object_id, **kwargs):
        external_listener = None
        if hasattr(request, "JSON"):
            confirm = request.JSON.get('confirm')
        else:
            confirm = request.POST.get('confirm')

        if confirm == 'yes':
            try:
                obj_inst = self.obj.objects.get(pk=object_id)
            except ObjectDoesNotExist:
                return HttpResponseNotFound('Object not found.')

            # Delete haproxy portal_*.cfg file if necessary
            if obj_inst.enable_external:
                for node in obj_inst.external_listener.get_nodes():
                    node.api_request("services.haproxy.haproxy.delete_conf", obj_inst.get_base_filename())
                external_listener = obj_inst.external_listener

            # Destroy dereferenced objects first
            obj_inst.delete()
            OpenIDRepository.objects.filter(client_id=obj_inst.oauth_client_id,
                                            client_secret=obj_inst.oauth_client_secret,
                                            provider="openid").delete()

            if external_listener:
                external_listener.reload_conf()

        if kwargs.get('api'):
            return JsonResponse({"status": True})
        return HttpResponseRedirect(self.redirect_url)


class DeleteLearningProfile(DeleteView):
    menu_name = _("Authentication -> Learning Profiles -> Delete")
    obj = LearningProfile
    redirect_url = "/authentication/learning_profiles/"
    delete_url = "/authentication/learning_profiles/delete/"

    # get, post and used_by methods herited from mother class


class DeleteTOTPProfile(DeleteView):
    menu_name = _("Authentication -> TOTP Profiles -> Delete")
    obj = TOTPProfile
    redirect_url = "/authentication/totp_profiles/"
    delete_url = "/authentication/totp_profiles/delete/"

    # get, post and used_by methods herited from mother class


class DeleteOpenIDRepository(DeleteView):
    menu_name = _("Authentication -> Repository OpenID -> Delete")
    obj = OpenIDRepository
    redirect_url = "/authentication/openid/"
    delete_url = "/authentication/openid/delete/"

    def used_by(self, object):
        return ["Portal " + portal.name for portal in UserAuthentication.objects.filter(repositories=object)]

    # get, post and used_by methods herited from mother class


class DeleteAuthAccessControl(DeleteView):
    menu_name = _("Authentication -> Access Control -> Delete")
    obj = AuthAccessControl
    redirect_url = "/portal/authentication/acl/"
    delete_url = "/portal/authentication/acl/delete/"

    def used_by(self, obj):
        return [str(w) for w in Workflow.objects.filter(authentication_filter=obj)]


class DeletePortalTemplate(DeleteView):
    menu_name = _("Authentication -> Portal Template -> Delete")
    obj = PortalTemplate
    redirect_url = "/portal/template/"
    delete_url = "/portal/template/delete/"

class DeletePortalImage(DeleteView):
    menu_name = _("Authentication -> Portal Template -> Delete")
    obj = TemplateImage
    redirect_url = "/portal/template/"
    delete_url = "/portal/images/delete/"


class DeleteUserScope(DeleteView):
    menu_name = _("Authentication -> User's Scope -> Delete")
    obj = UserScope
    redirect_url = "/authentication/user_scope/"
    delete_url = "/authentication/user_scope/delete/"

    def used_by(self, object):
        return [str(p) for p in object.userauthentication_set.all()]+[str(c) for c in object.openidrepository_set.all()]

