from django import template
from django.utils.safestring import mark_safe

from mainapp.models import Smartphone

register = template.Library()

TABLE_HEAD = """
                <table class="table">
                  <tbody>
             """

TABLE_TAIL = """
                  </tbody>
                </table>
             """

TABLE_CONTENT = """
                    <tr>
                      <td>{name}</td>
                      <td>{value}</td>
                    </tr>
                """

PRODUCT_SPEC = {
    'notebook': {
        'диагональ': 'diagonal',
        'Тип дисплея': 'display',
        'Частота процессора': 'processor_freq',
        'Оперативная память': 'ram',
        'Видеокарта': 'video',
        'Время работы аккумулятора': 'time_without_charge'
    },
    'smartphone': {
        'Оперативная память': 'ram',
        'диагональ': 'diagonal',
        'Тип дисплея': 'display',
        'Разрещение экрана': 'resolution',
        'Заряд аккумулятора': 'accum_volume',
        'Наличие слота для SD карты': 'sd',
        'максимальный обьём SD карты': 'sd_volume_max',
        'Камера (МП)': 'main_cam_mp',
        'Фронтальная камера (МП)': 'frontal_cam_mp'
    }
}


def get_product_spec(product, model_name):
    table_content = ''
    for name, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_CONTENT.format(name=name, value=getattr(product, value))
    return table_content


@register.filter
def product_spec(product):
    model_name = product.__class__._meta.model_name
    if isinstance(product, Smartphone):
        if not product.sd:
            PRODUCT_SPEC['smartphone'].pop('максимальный обьём SD карты')
        else:
            PRODUCT_SPEC['smartphone']['максимальный обьём SD карты'] = 'sd_volume_max'
    return mark_safe(TABLE_HEAD + get_product_spec(product, model_name) + TABLE_TAIL)
