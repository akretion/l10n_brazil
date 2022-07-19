# Copyright 2022-TODAY Akretion - Raphael Valyi <raphael.valyi@akretion.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).

from odoo.fields import Field, Selection


class FieldDecorator(Selection):  # TODO only inherit selection?
    _component = None

    def __init__(self, component) -> None:
        self._component = component

    @property
    def component(self):
        return self._component

    def _setup_base(self, model, name):    
        """ Base setup: things that do not depend on other models/fields. """
        if self._setup_done and not self.related:
            # optimization for regular fields: keep the base setup
            self._setup_done = 'base'
        else:
            # do the base setup from scratch
            self._setup_attrs(model, name)
            if not self.related:
                self._setup_regular_base(model)
            self._setup_done = 'base'

    def _setup_attrs(self, model, name):
        super(Selection, self)._setup_attrs(model, name)

        # determine selection (applying 'selection_add' extensions)
        values = None
        labels = {}

        for field in reversed(resolve_mro(model, name, self._can_setup_from)):
            # We cannot use field.selection or field.selection_add here
            # because those attributes are overridden by ``_setup_attrs``.
            if 'selection' in field.args:
                if self.related:
                  pass
                    #_logger.warning("%s: selection attribute will be ignored as the field is related", self)
                    #print(self, model, name)
#                    s
                selection = field.args['selection']
                if isinstance(selection, list):
                    if values is not None and values != [kv[0] for kv in selection]:
                        _logger.warning("%s: selection=%r overrides existing selection; use selection_add instead", self, selection)
                    values = [kv[0] for kv in selection]
                    labels = dict(selection)
                    self.ondelete = {}
                else:
                    values = None    
                    labels = {}
                    self.selection = selection
                    self.ondelete = None

            if 'selection_add' in field.args:
                if self.related:
                    _logger.warning("%s: selection_add attribute will be ignored as the field is related", self)
                selection_add = field.args['selection_add']
                assert isinstance(selection_add, list), \
                    "%s: selection_add=%r must be a list" % (self, selection_add)
                assert values is not None, \
                    "%s: selection_add=%r on non-list selection %r" % (self, selection_add, self.selection)

                ondelete = field.args.get('ondelete') or {}
                new_values = [kv[0] for kv in selection_add if kv[0] not in values]
                for key in new_values:
                    ondelete.setdefault(key, 'set null')
                if self.required and new_values and 'set null' in ondelete.values():
                    raise ValueError(
                        "%r: required selection fields must define an ondelete policy that "
                        "implements the proper cleanup of the corresponding records upon "
                        "module uninstallation. Please use one or more of the following "
                        "policies: 'set default' (if the field has a default defined), 'cascade', "
                        "or a single-argument callable where the argument is the recordset "
                        "containing the specified option." % self
                    )

                # check ondelete values
                for key, val in ondelete.items():
                    if callable(val) or val in ('set null', 'cascade'):
                        continue
                    if val == 'set default':
                        assert self.default is not None, (
                            "%r: ondelete policy of type 'set default' is invalid for this field "
                            "as it does not define a default! Either define one in the base "
                            "field, or change the chosen ondelete policy" % self
                        )
                        continue
                    raise ValueError(
                        "%r: ondelete policy %r for selection value %r is not a valid ondelete "
                        "policy, please choose one of 'set null', 'set default', 'cascade' or "
                        "a callable" % (self, val, key)
                    )

                values = merge_sequences(values, [kv[0] for kv in selection_add])
                labels.update(kv for kv in selection_add if len(kv) == 2)
                self.ondelete.update(ondelete)

        if values is not None:
            self.selection = [(value, labels[value]) for value in values]

    # Two methods we don't actually want to intercept,
    # but iter() and next() will be upset without them.

    def __iter__(self):
        return self._component.__iter__()

    def __next__(self):
        return self._component.__next__()

    # Offer every other method and property dynamically.

    def __getattr__(self, name):
        print("wwwwwww", name)
        return getattr(self._component, name)

    def __setattr__(self, name, value):
        if name in ('_component', '_logger'):
            self.__dict__[name] = value
        else:
            setattr(self._component, name, value)

    def __delattr__(self, name):
        delattr(self._component, name)
