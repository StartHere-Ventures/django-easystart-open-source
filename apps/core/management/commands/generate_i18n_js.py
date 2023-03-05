"""Command to generate JavaScript file used for i18n on the frontend"""

import json
import os
import uuid

from django.conf import settings
from django.core.management.base import BaseCommand
from django.template import Context, Engine
from django.utils.translation.trans_real import DjangoTranslation
from django.views.i18n import JavaScriptCatalog, get_formats

from utils.build_dict_language import get_array_language

js_catalog_template = r"""
{% autoescape off %}
(function(globals) {
  var activeLang = navigator.language || navigator.userLanguage || 'en';
  var activeLang = activeLang.substring(0,2)
  var django = globals.django || (globals.django = {});
  var plural = {{ plural }};
  django.pluralidx = function(n) {
    var v = plural[activeLang];
    if(v){
        if (typeof(v) == 'boolean') {
          return v ? 1 : 0;
        } else {
          return v;
        }
    } else {
        return (n == 1) ? 0 : 1;
    }
  };
  /* gettext library */
  django.catalog = django.catalog || {};
  {% if catalog_str %}
  var newcatalog = {{ catalog_str }};
  for (var ln in newcatalog) {
    django.catalog[ln] = newcatalog[ln];
  }
  {% endif %}
  if (!django.jsi18n_initialized) {
    django.setlang = function(lang){
        if(lang){
            activeLang = lang;
        }
    }

    django.gettext = function(msgid) {
      var lnCatalog = django.catalog[activeLang];
      if(lnCatalog){
          var value = lnCatalog[msgid];
          if (typeof(value) != 'undefined') {
            return (typeof(value) == 'string') ? value : value[0];
          }
      }
      return msgid;
    };
    django.ngettext = function(singular, plural, count) {
      var lnCatalog = django.catalog[activeLang]
      if(lnCatalog){
          var value = lnCatalog[singular];
          if (typeof(value) != 'undefined') {
          } else {
            return value.constructor === Array ? value[django.pluralidx(count)] : value;
          }
      }
      return (count == 1) ? singular : plural;
    };
    django.gettext_noop = function(msgid) { return msgid; };
    django.pgettext = function(context, msgid) {
      var value = django.gettext(context + '\x04' + msgid);
      if (value.indexOf('\x04') != -1) {
        value = msgid;
      }
      return value;
    };
    django.npgettext = function(context, singular, plural, count) {
      var value = django.ngettext(context + '\x04' + singular, context + '\x04' + plural, count);
      if (value.indexOf('\x04') != -1) {
        value = django.ngettext(singular, plural, count);
      }
      return value;
    };
    django.interpolate = function(fmt, obj, named) {
      if (named) {
        return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
      } else {
        return fmt.replace(/%s/g, function(match){return String(obj.shift())});
      }
    };
    /* formatting library */
    django.formats = {{ formats_str }};
    django.get_format = function(format_type) {
      var value = django.formats[format_type];
      if (typeof(value) == 'undefined') {
        return format_type;
      } else {
        return value;
      }
    };
    /* add to global namespace */
    globals.setlang = django.setlang;
    globals.pluralidx = django.pluralidx;
    globals.gettext = django.gettext;
    globals.ngettext = django.ngettext;
    globals.gettext_noop = django.gettext_noop;
    globals.pgettext = django.pgettext;
    globals.npgettext = django.npgettext;
    globals.interpolate = django.interpolate;
    globals.get_format = django.get_format;
    django.jsi18n_initialized = true;
  }
}(this));
{% endautoescape %}
"""


class Command(BaseCommand):
    """Generate JavaScript file for i18n purposes"""

    help = "Generate JavaScript file for i18n purposes"

    def add_arguments(self, parser):
        parser.add_argument("PATH", nargs=1, type=str)

    def handle(self, *args, **options):
        packages = getattr(settings, "JS_INFO_DICT", None)
        if packages is not None:
            packages = packages["packages"]

        contents = self.generate_i18n_js(packages)
        path = os.path.join(settings.BASE_DIR, options["PATH"][0])
        js_name = f"translation-{str(uuid.uuid4()).split('-')[-1]}.js"
        new_path = os.path.join(path, js_name)
        # Create directory if not exist
        try:
            os.mkdir(path)
        except FileExistsError:
            pass

        # Remove files into path
        self.remove_files(path)

        with open(new_path, "w") as f:
            f.write(contents)
        self.stdout.write("wrote file into %s\n" % new_path)

        self.generate_stats(options["PATH"][0], js_name)

    def generate_stats(self, path, file_name):
        json_content = {"status": "done", "file": file_name, "publicPath": path}
        path = os.path.join(settings.BASE_DIR, "translation-stats.json")
        with open(path, "w") as f:
            f.write(json.dumps(json_content))
        self.stdout.write("wrote manifies into %s\n" % path)

    def remove_files(self, path):
        os.chdir(path)
        for root, dirs, files in os.walk(".", topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))

    def generate_i18n_js(self, packs):
        class InlineJavaScriptCatalog(JavaScriptCatalog):
            def render_to_str(self):
                # hardcoding locales as it is not trivial to
                # get user apps and its locales, and including
                # all django supported locales is not efficient
                packages = packs if packs else self.packages
                paths = self.get_paths(packages) if packages else None

                codes = get_array_language()
                catalog = {}
                plural = {}
                # this function is not i18n-enabled
                formats = get_formats()
                for code in codes:
                    self.translation = DjangoTranslation(
                        code, domain=self.domain, localedirs=paths
                    )
                    _catalog = self.get_catalog()
                    _plural = self.get_plural()
                    if _catalog:
                        catalog[code] = _catalog
                    if _plural:
                        plural[code] = _plural
                template = Engine().from_string(js_catalog_template)
                context = {
                    "catalog_str": json.dumps(catalog, sort_keys=True, indent=2),
                    "formats_str": json.dumps(formats, sort_keys=True, indent=2),
                    "plural": plural,
                }
                return template.render(Context(context))

        return InlineJavaScriptCatalog().render_to_str()
