#!/usr/bin/env python
import os
import sys
from django.utils import timezone
from datetime import datetime, timedelta

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kulik.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


from discount.models import Product
from django.db.models import F, Q
from datetime import date

#p = Product.objects.get(normal_price__gte=F('normal_price') - F('stock_price'), pk=1)
#p = Product.objects.get(normal_price__gte=F('stock_price'), pk=1)
"""
p = Product.objects.get(
    #pk=1,
    Q(pk=1) & Q(pk__lte=2),
    #Q(title__startswith='П'),
    #Q(created__gte=date(2005, 5, 2)) | Q(created__lte=date(2005, 5, 6))
)
print(p)
"""

#q = Q(pk=1) & ~Q(pk=2)
#print(q)


"""
from django.utils import tree
n1 = tree.Node(children=[1, 2])
n2 = tree.Node(children=[2, 3])
n2.negate()
n1.add(n2, 'ADD')
n1.add([1, 2], 'REMOVE')
print(n1)
"""
"""

q = Q(f)
print(q)
"""


#https://docs.djangoproject.com/en/1.8/howto/custom-lookups/
#***********************
from django.db.models import Lookup

class NotEqual(Lookup):
    lookup_name = 'ne'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return '%s <> %s' % (lhs, rhs), params


from django.db.models import Transform

class AbsoluteValue(Transform):
    lookup_name = 'abs'

    def as_sql(self, compiler, connection):
        lhs, params = compiler.compile(self.lhs)
        return "ABS(%s)" % lhs, params

from django.db.models import IntegerField
IntegerField.register_lookup(AbsoluteValue)
#*******************************

from django.db.models import Transform, FloatField, Lookup

class NegativeValue(Transform):
    lookup_name = 'ne'
    def as_sql(self, compiler, connection):
        lhs, params = compiler.compile(self.lhs) #Сравнить с process_lhs
        return '-1 * %s' % lhs, params

    @property
    def output_field(self):
        return IntegerField()


class NextTo(Lookup):
    lookup_name = 'nt'
    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return 'ABS(%s + %s) < 10' % (lhs, rhs), params

#************************************************

from django.db.models import IntegerField
IntegerField.register_lookup(NegativeValue)
IntegerField.register_lookup(NextTo)


from django.db.models import IntegerField, Transform
from django.db.models import Lookup

class AbsoluteValue(Transform):
    lookup_name = 'abs'

    def as_sql(self, compiler, connection):
        lhs, params = compiler.compile(self.lhs)
        return "ABS(%s)" % lhs, params

    @property
    def output_field(self):
        return IntegerField()




class AbsoluteValueLessThan(Lookup):
    lookup_name = 'lt'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = compiler.compile(self.lhs.lhs) #Обратимся напрямую к lhs
        #lhs, lhs_params = self.process_lhs(compiler, connection) # Вызовет AbsoluteValue.as_sql, но нам тут этого не нужно.
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params + lhs_params + rhs_params
        return '%s < %s AND %s > -%s' % (lhs, rhs, lhs, rhs), params

IntegerField.register_lookup(AbsoluteValue)
AbsoluteValue.register_lookup(AbsoluteValueLessThan)



#************************************************

from django.db.models import Transform, Field

class UpperCase(Transform):
    lookup_name = 'upper'
    bilateral = True

    def as_sql(self, compiler, connection):
        lhs, params = compiler.compile(self.lhs)
        return "UPPER(%s)" % lhs, params

from django.db.models import CharField, TextField
CharField.register_lookup(UpperCase)
TextField.register_lookup(UpperCase)


class AbsoluteValue(Transform):
    lookup_name = 'abs'

    def as_sql(self, compiler, connection):
        lhs, params = compiler.compile(self.lhs)
        return "ABS(%s)" % lhs, params

    @property
    def output_field(self):
        return FloatField()

#*****************************8

class CoordinatesField(Field):
    def get_lookup(self, lookup_name):
        if lookup_name.startswith('x'):
            try:
                dimension = int(lookup_name[1:])
            except ValueError:
                pass
            finally:
                return get_coordinate_lookup(dimension)
        return super(CoordinatesField, self).get_lookup(lookup_name)


def get_coordinate_lookup(dimension):
    class CoordinateLookup(Lookup):

        def as_sql(self, compiler, connection):
            lhs, lhs_params = self.process_lhs(compiler, connection)
            rhs, rhs_params = self.process_rhs(compiler, connection)
            params = lhs_params + rhs_params
            return '%s = %s * %s' % (lhs, rhs, dimension), params

    return CoordinateLookup


class CoordinateValue(Transform):
    lookup_name = 'coord'

    def as_sql(self, compiler, connection):
        lhs, params = compiler.compile(self.lhs)
        return "%s" % lhs, params

    @property
    def output_field(self):
        return CoordinatesField()
Field.register_lookup(CoordinateValue)

p = Product.objects.get(stock_price__coord__x2=500)
print(p)

#**********************************************************************
#Expressions


from discount.models import Product
from django.db.models import F, Q, Count, Value, DateTimeField, ExpressionWrapper, Func, Aggregate, IntegerField, CharField
from django.db.models.functions import Length #???

from datetime import date

#https://docs.djangoproject.com/en/1.8/ref/models/expressions/


p = Product.objects.get(pk=1)
p.normal_price = F('normal_price') + 1
p.save()

ps = Product.objects.filter(stock_price__lte=F('normal_price') - 11)

ps = ps.filter(~Q(stock_price__lte=F('normal_price') - 11))

ps = Product.objects.filter(stock_price__lte=(F('normal_price') +F('stock_price')))

ps = Product.objects.annotate(diff=F('normal_price') - F('stock_price')).filter(diff__lte=F('stock_price'))

ps = Product.objects.annotate(ptcs=Count(F('cart_products'))).filter(ptcs__gte=2) #Можно без F

ps = Product.objects.order_by(Length('title').desc())

ps = Product.objects.annotate(moved_created=ExpressionWrapper(F('created') + timezone.timedelta(days=2), output_field=DateTimeField())) #Поскольку поля разных типов, нужен ExpressionWrapper и указание в каком формате результат

ps = Product.objects.annotate(lower_title=Func(F('title'), function='LOWER')).filter(lower_title__contains='ж')


class Lower(Func):
    function = 'LOWER'
    template = '%(function)s(%(expressions)s)' # - не обязательно

ps = Product.objects.annotate(lower_title=Lower(F('title')))
ps = Product.objects.annotate(lower_title=Lower('title'))

ps = Product.objects.annotate(num=Count('cart_products') / 2 + Count(F('cart_products')))


class MyCount(Aggregate):
    # supports COUNT(distinct field)
    function = 'COUNT'
    template = '%(function)s(%(distinct)s%(expressions)s)'

    def __init__(self, expression, distinct=False, **extra):
        super().__init__(
            expression,
            distinct='DISTINCT ' if distinct else '',
            output_field=IntegerField(),
            **extra)

ps = Product.objects.annotate(num=MyCount('cart_products') / 2 + Count(F('cart_products')))

print(ps)


from django.db.models import Expression

class Coalesce(Expression):
    template = 'COALESCE( %(expressions)s )'

    def __init__(self, expressions, output_field, **extra):
      super(Coalesce, self).__init__(output_field=output_field)
      if len(expressions) < 2:
          raise ValueError('expressions must have at least 2 elements')
      for expression in expressions:
          if not hasattr(expression, 'resolve_expression'):
              raise TypeError('%r is not an Expression' % expression)
      self.expressions = expressions
      self.extra = extra

    def resolve_expression(self, query=None, allow_joins=True, reuse=None, summarize=False):
        c = self.copy()
        c.is_summary = summarize
        for pos, expression in enumerate(self.expressions):
            c.expressions[pos] = expression.resolve_expression(query, allow_joins, reuse, summarize)
        return c

    def as_sql(self, compiler, connection):
        sql_expressions, sql_params = [], []
        for expression in self.expressions:
            sql, params = compiler.compile(expression)
            sql_expressions.append(sql)
            sql_params.extend(params)
        self.extra['expressions'] = ','.join(sql_expressions)
        return self.template % self.extra, sql_params

    def as_oracle(self, compiler, connection):
        """
        Example of vendor specific handling (Oracle in this case).
        Let's make the function name lowercase.
        """
        self.template = 'coalesce( %(expressions)s )'
        return self.as_sql(compiler, connection)



qs = Product.objects.annotate(
    tagline=Coalesce([
       F('body'),
       F('title'),
       Value('No Tagline')
       ], output_field=CharField()))

for c in qs:
    print("%s: %s" % (c.title, c.tagline))



#************************************************
from discount.models import Product
from django.db.models import F, Q, Count, Value, DateTimeField, ExpressionWrapper, \
    Func, Aggregate, IntegerField, CharField, When, Case, Sum
from django.db.models.functions import Length #???

ps = Product.objects.annotate(countains_j=Case(
    When(title__contains='ж', then=1),
    When(Q(title__contains='я'), then=2),
    #default = 0,
    default=Value(0),
    output_field=IntegerField()))
for p in ps:
    print('%s - %s' % (p.title, p.countains_j))


Product.objects.update(tatamo_comment=
    Case(
    When(title__contains='ж', then=Value(1)),
    When(Q(title__contains='я'), then=2),
    #default = 0,
    default=Value(0),
    output_field=IntegerField()
    )
)

ps = Product.objects.all()
"""
for p in ps:
    print('%s - %s' % (p.title, p.tatamo_comment))
"""

ps = Product.objects.aggregate(
    cheap=
    Sum(
        Case(
            When(stock_price__lte=300, then=1),
            output_field=IntegerField(),
        )
    ),
    middle=
    Sum(
        Case(
            When(stock_price__gt=300, stock_price__lte=1000, then=1),
            output_field=IntegerField()
            )
        ),
    expensive=
    Sum(
        Case(
            When(stock_price__gt=1000, then=1),
            output_field=IntegerField()
        )
    )
        )
print(ps)
#{'middle': 75, 'cheap': 53, 'expensive': 1591}

ps = Product.objects.annotate(
    ptcs=
    Coalesce(  #Нет смысла, но для примера
    Sum(
        Case(
            When(cart_products__status=1, then=1),
            default=0,
            output_field=IntegerField()
        )
    ),
     Value(0)
        )
)

for p in ps:
    print('%s - %s' % (p.title, p.ptcs))


#*************************************************


from discount.models import Product
from django.db.models import F, Q, Count, Value, DateTimeField, ExpressionWrapper, \
    Func, Aggregate, IntegerField, CharField, When, Case, Sum



from django.db.models import Sum, Value as V
from django.db.models.functions import Coalesce, Concat, Length, Lower, Upper, Substr

ps = Product.objects.annotate(coa=Coalesce('tatamo_comment', F('title'), 'body', output_field=CharField()))

ps = Product.objects.annotate(con=Concat('tatamo_comment', F('title'), 'body', output_field=CharField()))

ps = Product.objects.annotate(l1=Length('tatamo_comment'),
                              l2=
                              Coalesce(
                                  Length(
                                      F('shop_comment')), Value(0))
                              )

ps = Product.objects.annotate(lt=Lower('title'))

ps = Product.objects.annotate(ut=Upper(F('title')))

ps = Product.objects.annotate(st=Substr('title', 1, 3))

for p in ps:
    print('%s - %s' % (p.title, p.st))