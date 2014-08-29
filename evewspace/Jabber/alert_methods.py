from Alerts.method_registry import registry
from jabber_method import JabberAlertMethod
from slack_method import SlackAlertMethod
registry.register("Jabber", JabberAlertMethod)
registry.register("Slack", SlackAlertMethod)
