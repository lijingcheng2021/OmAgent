import pprint
import re  # noqa: F401

import six


class WorkflowSchedule(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        "name": "str",
        "cron_expression": "str",
        "run_catchup_schedule_instances": "bool",
        "paused": "bool",
        "start_workflow_request": "StartWorkflowRequest",
        "schedule_start_time": "int",
        "schedule_end_time": "int",
        "create_time": "int",
        "updated_time": "int",
        "created_by": "str",
        "updated_by": "str",
    }

    attribute_map = {
        "name": "name",
        "cron_expression": "cronExpression",
        "run_catchup_schedule_instances": "runCatchupScheduleInstances",
        "paused": "paused",
        "start_workflow_request": "startWorkflowRequest",
        "schedule_start_time": "scheduleStartTime",
        "schedule_end_time": "scheduleEndTime",
        "create_time": "createTime",
        "updated_time": "updatedTime",
        "created_by": "createdBy",
        "updated_by": "updatedBy",
    }

    def __init__(
        self,
        name=None,
        cron_expression=None,
        run_catchup_schedule_instances=None,
        paused=None,
        start_workflow_request=None,
        schedule_start_time=None,
        schedule_end_time=None,
        create_time=None,
        updated_time=None,
        created_by=None,
        updated_by=None,
    ):  # noqa: E501
        """WorkflowSchedule - a model defined in Swagger"""  # noqa: E501
        self._name = None
        self._cron_expression = None
        self._run_catchup_schedule_instances = None
        self._paused = None
        self._start_workflow_request = None
        self._schedule_start_time = None
        self._schedule_end_time = None
        self._create_time = None
        self._updated_time = None
        self._created_by = None
        self._updated_by = None
        self.discriminator = None
        if name is not None:
            self.name = name
        if cron_expression is not None:
            self.cron_expression = cron_expression
        if run_catchup_schedule_instances is not None:
            self.run_catchup_schedule_instances = run_catchup_schedule_instances
        if paused is not None:
            self.paused = paused
        if start_workflow_request is not None:
            self.start_workflow_request = start_workflow_request
        if schedule_start_time is not None:
            self.schedule_start_time = schedule_start_time
        if schedule_end_time is not None:
            self.schedule_end_time = schedule_end_time
        if create_time is not None:
            self.create_time = create_time
        if updated_time is not None:
            self.updated_time = updated_time
        if created_by is not None:
            self.created_by = created_by
        if updated_by is not None:
            self.updated_by = updated_by

    @property
    def name(self):
        """Gets the name of this WorkflowSchedule.  # noqa: E501


        :return: The name of this WorkflowSchedule.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this WorkflowSchedule.


        :param name: The name of this WorkflowSchedule.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def cron_expression(self):
        """Gets the cron_expression of this WorkflowSchedule.  # noqa: E501


        :return: The cron_expression of this WorkflowSchedule.  # noqa: E501
        :rtype: str
        """
        return self._cron_expression

    @cron_expression.setter
    def cron_expression(self, cron_expression):
        """Sets the cron_expression of this WorkflowSchedule.


        :param cron_expression: The cron_expression of this WorkflowSchedule.  # noqa: E501
        :type: str
        """

        self._cron_expression = cron_expression

    @property
    def run_catchup_schedule_instances(self):
        """Gets the run_catchup_schedule_instances of this WorkflowSchedule.  # noqa: E501


        :return: The run_catchup_schedule_instances of this WorkflowSchedule.  # noqa: E501
        :rtype: bool
        """
        return self._run_catchup_schedule_instances

    @run_catchup_schedule_instances.setter
    def run_catchup_schedule_instances(self, run_catchup_schedule_instances):
        """Sets the run_catchup_schedule_instances of this WorkflowSchedule.


        :param run_catchup_schedule_instances: The run_catchup_schedule_instances of this WorkflowSchedule.  # noqa: E501
        :type: bool
        """

        self._run_catchup_schedule_instances = run_catchup_schedule_instances

    @property
    def paused(self):
        """Gets the paused of this WorkflowSchedule.  # noqa: E501


        :return: The paused of this WorkflowSchedule.  # noqa: E501
        :rtype: bool
        """
        return self._paused

    @paused.setter
    def paused(self, paused):
        """Sets the paused of this WorkflowSchedule.


        :param paused: The paused of this WorkflowSchedule.  # noqa: E501
        :type: bool
        """

        self._paused = paused

    @property
    def start_workflow_request(self):
        """Gets the start_workflow_request of this WorkflowSchedule.  # noqa: E501


        :return: The start_workflow_request of this WorkflowSchedule.  # noqa: E501
        :rtype: StartWorkflowRequest
        """
        return self._start_workflow_request

    @start_workflow_request.setter
    def start_workflow_request(self, start_workflow_request):
        """Sets the start_workflow_request of this WorkflowSchedule.


        :param start_workflow_request: The start_workflow_request of this WorkflowSchedule.  # noqa: E501
        :type: StartWorkflowRequest
        """

        self._start_workflow_request = start_workflow_request

    @property
    def schedule_start_time(self):
        """Gets the schedule_start_time of this WorkflowSchedule.  # noqa: E501


        :return: The schedule_start_time of this WorkflowSchedule.  # noqa: E501
        :rtype: int
        """
        return self._schedule_start_time

    @schedule_start_time.setter
    def schedule_start_time(self, schedule_start_time):
        """Sets the schedule_start_time of this WorkflowSchedule.


        :param schedule_start_time: The schedule_start_time of this WorkflowSchedule.  # noqa: E501
        :type: int
        """

        self._schedule_start_time = schedule_start_time

    @property
    def schedule_end_time(self):
        """Gets the schedule_end_time of this WorkflowSchedule.  # noqa: E501


        :return: The schedule_end_time of this WorkflowSchedule.  # noqa: E501
        :rtype: int
        """
        return self._schedule_end_time

    @schedule_end_time.setter
    def schedule_end_time(self, schedule_end_time):
        """Sets the schedule_end_time of this WorkflowSchedule.


        :param schedule_end_time: The schedule_end_time of this WorkflowSchedule.  # noqa: E501
        :type: int
        """

        self._schedule_end_time = schedule_end_time

    @property
    def create_time(self):
        """Gets the create_time of this WorkflowSchedule.  # noqa: E501


        :return: The create_time of this WorkflowSchedule.  # noqa: E501
        :rtype: int
        """
        return self._create_time

    @create_time.setter
    def create_time(self, create_time):
        """Sets the create_time of this WorkflowSchedule.


        :param create_time: The create_time of this WorkflowSchedule.  # noqa: E501
        :type: int
        """

        self._create_time = create_time

    @property
    def updated_time(self):
        """Gets the updated_time of this WorkflowSchedule.  # noqa: E501


        :return: The updated_time of this WorkflowSchedule.  # noqa: E501
        :rtype: int
        """
        return self._updated_time

    @updated_time.setter
    def updated_time(self, updated_time):
        """Sets the updated_time of this WorkflowSchedule.


        :param updated_time: The updated_time of this WorkflowSchedule.  # noqa: E501
        :type: int
        """

        self._updated_time = updated_time

    @property
    def created_by(self):
        """Gets the created_by of this WorkflowSchedule.  # noqa: E501


        :return: The created_by of this WorkflowSchedule.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this WorkflowSchedule.


        :param created_by: The created_by of this WorkflowSchedule.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def updated_by(self):
        """Gets the updated_by of this WorkflowSchedule.  # noqa: E501


        :return: The updated_by of this WorkflowSchedule.  # noqa: E501
        :rtype: str
        """
        return self._updated_by

    @updated_by.setter
    def updated_by(self, updated_by):
        """Sets the updated_by of this WorkflowSchedule.


        :param updated_by: The updated_by of this WorkflowSchedule.  # noqa: E501
        :type: str
        """

        self._updated_by = updated_by

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (
                            (item[0], item[1].to_dict())
                            if hasattr(item[1], "to_dict")
                            else item
                        ),
                        value.items(),
                    )
                )
            else:
                result[attr] = value
        if issubclass(WorkflowSchedule, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, WorkflowSchedule):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
