import grokcore.component
import zope.configuration.fields
import zope.interface


def _(x):
    return str(x)  # no i18n-ing for now.


class IErrorReportingUtilityDirective(zope.interface.Interface):
    """Register a error reporting utility.
    """

    factory = zope.configuration.fields.GlobalObject(
        title=_("Error reporting utility factory"),
        description=_(
            'The factory used to create the error reporting utility.'),
        required=True,
    )

    info_level_errors = zope.configuration.fields.Tokens(
        title=_('INFO-level errors'),
        description=_(
            'Exception (base)classes for errors that should be '
            'reported at "INFO" level.'),
        required=True,
        value_type=zope.configuration.fields.GlobalObject(
            missing_value=object()),
    )

    warning_level_errors = zope.configuration.fields.Tokens(
        title=_('WARNING-level errors'),
        description=_(
            'Exception (base)classes for errors that should be '
            'reported at "WARNING" level.'),
        required=True,
        value_type=zope.configuration.fields.GlobalObject(
            missing_value=object()),
    )

    always_exc_info = zope.configuration.fields.Bool(
        title=_("Always emit exc_info"),
        description=_(
            'When set to True, the exc_info of the error being logged is '
            'always passed on onto the log handler. The handler can decide '
            'what to do with the exc_info. The file-based log handler will '
            'append the stack trace information to the log record. Set to '
            'False if you do not want this exc_info passed on to the log '
            'handler for the info- and warning-level errors.'),
        default=False,
        required=False,
    )


def errorreportingutility(
        _context,
        factory=None,
        info_level_errors=(),
        warning_level_errors=(),
        always_exc_info=False,
        name=''):
    provides = zope.interface.implementedBy(factory)
    component = factory(
        tuple(info_level_errors),
        tuple(warning_level_errors),
        always_exc_info)
    _context.action(
        discriminator=('utility', provides, name),
        callable=grokcore.component.provideUtility,
        args=(component, provides, name),
    )
