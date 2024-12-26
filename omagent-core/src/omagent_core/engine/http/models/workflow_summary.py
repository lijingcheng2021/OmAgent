import pprint
import re  # noqa: F401

import six


class WorkflowSummary(object):
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
        "workflow_type": "str",
        "version": "int",
        "workflow_id": "str",
        "correlation_id": "str",
        "start_time": "str",
        "update_time": "str",
        "end_time": "str",
        "status": "str",
        "input": "str",
        "output": "str",
        "reason_for_incompletion": "str",
        "execution_time": "int",
        "event": "str",
        "failed_reference_task_names": "str",
        "external_input_payload_storage_path": "str",
        "external_output_payload_storage_path": "str",
        "priority": "int",
        "created_by": "str",
        "output_size": "int",
        "input_size": "int",
    }

    attribute_map = {
        "workflow_type": "workflowType",
        "version": "version",
        "workflow_id": "workflowId",
        "correlation_id": "correlationId",
        "start_time": "startTime",
        "update_time": "updateTime",
        "end_time": "endTime",
        "status": "status",
        "input": "input",
        "output": "output",
        "reason_for_incompletion": "reasonForIncompletion",
        "execution_time": "executionTime",
        "event": "event",
        "failed_reference_task_names": "failedReferenceTaskNames",
        "external_input_payload_storage_path": "externalInputPayloadStoragePath",
        "external_output_payload_storage_path": "externalOutputPayloadStoragePath",
        "priority": "priority",
        "created_by": "createdBy",
        "output_size": "outputSize",
        "input_size": "inputSize",
    }

    def __init__(
        self,
        workflow_type=None,
        version=None,
        workflow_id=None,
        correlation_id=None,
        start_time=None,
        update_time=None,
        end_time=None,
        status=None,
        input=None,
        output=None,
        reason_for_incompletion=None,
        execution_time=None,
        event=None,
        failed_reference_task_names=None,
        external_input_payload_storage_path=None,
        external_output_payload_storage_path=None,
        priority=None,
        created_by=None,
        output_size=None,
        input_size=None,
    ):  # noqa: E501
        """WorkflowSummary - a model defined in Swagger"""  # noqa: E501
        self._workflow_type = None
        self._version = None
        self._workflow_id = None
        self._correlation_id = None
        self._start_time = None
        self._update_time = None
        self._end_time = None
        self._status = None
        self._input = None
        self._output = None
        self._reason_for_incompletion = None
        self._execution_time = None
        self._event = None
        self._failed_reference_task_names = None
        self._external_input_payload_storage_path = None
        self._external_output_payload_storage_path = None
        self._priority = None
        self._created_by = None
        self._output_size = None
        self._input_size = None
        self.discriminator = None
        if workflow_type is not None:
            self.workflow_type = workflow_type
        if version is not None:
            self.version = version
        if workflow_id is not None:
            self.workflow_id = workflow_id
        if correlation_id is not None:
            self.correlation_id = correlation_id
        if start_time is not None:
            self.start_time = start_time
        if update_time is not None:
            self.update_time = update_time
        if end_time is not None:
            self.end_time = end_time
        if status is not None:
            self.status = status
        if input is not None:
            self.input = input
        if output is not None:
            self.output = output
        if reason_for_incompletion is not None:
            self.reason_for_incompletion = reason_for_incompletion
        if execution_time is not None:
            self.execution_time = execution_time
        if event is not None:
            self.event = event
        if failed_reference_task_names is not None:
            self.failed_reference_task_names = failed_reference_task_names
        if external_input_payload_storage_path is not None:
            self.external_input_payload_storage_path = (
                external_input_payload_storage_path
            )
        if external_output_payload_storage_path is not None:
            self.external_output_payload_storage_path = (
                external_output_payload_storage_path
            )
        if priority is not None:
            self.priority = priority
        if created_by is not None:
            self.created_by = created_by
        if output_size is not None:
            self.output_size = output_size
        if input_size is not None:
            self.input_size = input_size

    @property
    def workflow_type(self):
        """Gets the workflow_type of this WorkflowSummary.  # noqa: E501


        :return: The workflow_type of this WorkflowSummary.  # noqa: E501
        :rtype: str
        """
        return self._workflow_type

    @workflow_type.setter
    def workflow_type(self, workflow_type):
        """Sets the workflow_type of this WorkflowSummary.


        :param workflow_type: The workflow_type of this WorkflowSummary.  # noqa: E501
        :type: str
        """

        self._workflow_type = workflow_type

    @property
    def version(self):
        """Gets the version of this WorkflowSummary.  # noqa: E501


        :return: The version of this WorkflowSummary.  # noqa: E501
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this WorkflowSummary.


        :param version: The version of this WorkflowSummary.  # noqa: E501
        :type: int
        """

        self._version = version

    @property
    def workflow_id(self):
        """Gets the workflow_id of this WorkflowSummary.  # noqa: E501


        :return: The workflow_id of this WorkflowSummary.  # noqa: E501
        :rtype: str
        """
        return self._workflow_id

    @workflow_id.setter
    def workflow_id(self, workflow_id):
        """Sets the workflow_id of this WorkflowSummary.


        :param workflow_id: The workflow_id of this WorkflowSummary.  # noqa: E501
        :type: str
        """

        self._workflow_id = workflow_id

    @property
    def correlation_id(self):
        """Gets the correlation_id of this WorkflowSummary.  # noqa: E501


        :return: The correlation_id of this WorkflowSummary.  # noqa: E501
        :rtype: str
        """
        return self._correlation_id

    @correlation_id.setter
    def correlation_id(self, correlation_id):
        """Sets the correlation_id of this WorkflowSummary.


        :param correlation_id: The correlation_id of this WorkflowSummary.  # noqa: E501
        :type: str
        """

        self._correlation_id = correlation_id

    @property
    def start_time(self):
        """Gets the start_time of this WorkflowSummary.  # noqa: E501


        :return: The start_time of this WorkflowSummary.  # noqa: E501
        :rtype: str
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this WorkflowSummary.


        :param start_time: The start_time of this WorkflowSummary.  # noqa: E501
        :type: str
        """

        self._start_time = start_time

    @property
    def update_time(self):
        """Gets the update_time of this WorkflowSummary.  # noqa: E501


        :return: The update_time of this WorkflowSummary.  # noqa: E501
        :rtype: str
        """
        return self._update_time

    @update_time.setter
    def update_time(self, update_time):
        """Sets the update_time of this WorkflowSummary.


        :param update_time: The update_time of this WorkflowSummary.  # noqa: E501
        :type: str
        """

        self._update_time = update_time

    @property
    def end_time(self):
        """Gets the end_time of this WorkflowSummary.  # noqa: E501


        :return: The end_time of this WorkflowSummary.  # noqa: E501
        :rtype: str
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """Sets the end_time of this WorkflowSummary.


        :param end_time: The end_time of this WorkflowSummary.  # noqa: E501
        :type: str
        """

        self._end_time = end_time

    @property
    def status(self):
        """Gets the status of this WorkflowSummary.  # noqa: E501


        :return: The status of this WorkflowSummary.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this WorkflowSummary.


        :param status: The status of this WorkflowSummary.  # noqa: E501
        :type: str
        """
        allowed_values = [
            "RUNNING",
            "COMPLETED",
            "FAILED",
            "TIMED_OUT",
            "TERMINATED",
            "PAUSED",
        ]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}".format(  # noqa: E501
                    status, allowed_values
                )
            )

        self._status = status

    @property
    def input(self):
        """Gets the input of this WorkflowSummary.  # noqa: E501


        :return: The input of this WorkflowSummary.  # noqa: E501
        :rtype: str
        """
        return self._input

    @input.setter
    def input(self, input):
        """Sets the input of this WorkflowSummary.


        :param input: The input of this WorkflowSummary.  # noqa: E501
        :type: str
        """

        self._input = input

    @property
    def output(self):
        """Gets the output of this WorkflowSummary.  # noqa: E501


        :return: The output of this WorkflowSummary.  # noqa: E501
        :rtype: str
        """
        return self._output

    @output.setter
    def output(self, output):
        """Sets the output of this WorkflowSummary.


        :param output: The output of this WorkflowSummary.  # noqa: E501
        :type: str
        """

        self._output = output

    @property
    def reason_for_incompletion(self):
        """Gets the reason_for_incompletion of this WorkflowSummary.  # noqa: E501


        :return: The reason_for_incompletion of this WorkflowSummary.  # noqa: E501
        :rtype: str
        """
        return self._reason_for_incompletion

    @reason_for_incompletion.setter
    def reason_for_incompletion(self, reason_for_incompletion):
        """Sets the reason_for_incompletion of this WorkflowSummary.


        :param reason_for_incompletion: The reason_for_incompletion of this WorkflowSummary.  # noqa: E501
        :type: str
        """

        self._reason_for_incompletion = reason_for_incompletion

    @property
    def execution_time(self):
        """Gets the execution_time of this WorkflowSummary.  # noqa: E501


        :return: The execution_time of this WorkflowSummary.  # noqa: E501
        :rtype: int
        """
        return self._execution_time

    @execution_time.setter
    def execution_time(self, execution_time):
        """Sets the execution_time of this WorkflowSummary.


        :param execution_time: The execution_time of this WorkflowSummary.  # noqa: E501
        :type: int
        """

        self._execution_time = execution_time

    @property
    def event(self):
        """Gets the event of this WorkflowSummary.  # noqa: E501


        :return: The event of this WorkflowSummary.  # noqa: E501
        :rtype: str
        """
        return self._event

    @event.setter
    def event(self, event):
        """Sets the event of this WorkflowSummary.


        :param event: The event of this WorkflowSummary.  # noqa: E501
        :type: str
        """

        self._event = event

    @property
    def failed_reference_task_names(self):
        """Gets the failed_reference_task_names of this WorkflowSummary.  # noqa: E501


        :return: The failed_reference_task_names of this WorkflowSummary.  # noqa: E501
        :rtype: str
        """
        return self._failed_reference_task_names

    @failed_reference_task_names.setter
    def failed_reference_task_names(self, failed_reference_task_names):
        """Sets the failed_reference_task_names of this WorkflowSummary.


        :param failed_reference_task_names: The failed_reference_task_names of this WorkflowSummary.  # noqa: E501
        :type: str
        """

        self._failed_reference_task_names = failed_reference_task_names

    @property
    def external_input_payload_storage_path(self):
        """Gets the external_input_payload_storage_path of this WorkflowSummary.  # noqa: E501


        :return: The external_input_payload_storage_path of this WorkflowSummary.  # noqa: E501
        :rtype: str
        """
        return self._external_input_payload_storage_path

    @external_input_payload_storage_path.setter
    def external_input_payload_storage_path(self, external_input_payload_storage_path):
        """Sets the external_input_payload_storage_path of this WorkflowSummary.


        :param external_input_payload_storage_path: The external_input_payload_storage_path of this WorkflowSummary.  # noqa: E501
        :type: str
        """

        self._external_input_payload_storage_path = external_input_payload_storage_path

    @property
    def external_output_payload_storage_path(self):
        """Gets the external_output_payload_storage_path of this WorkflowSummary.  # noqa: E501


        :return: The external_output_payload_storage_path of this WorkflowSummary.  # noqa: E501
        :rtype: str
        """
        return self._external_output_payload_storage_path

    @external_output_payload_storage_path.setter
    def external_output_payload_storage_path(
        self, external_output_payload_storage_path
    ):
        """Sets the external_output_payload_storage_path of this WorkflowSummary.


        :param external_output_payload_storage_path: The external_output_payload_storage_path of this WorkflowSummary.  # noqa: E501
        :type: str
        """

        self._external_output_payload_storage_path = (
            external_output_payload_storage_path
        )

    @property
    def priority(self):
        """Gets the priority of this WorkflowSummary.  # noqa: E501


        :return: The priority of this WorkflowSummary.  # noqa: E501
        :rtype: int
        """
        return self._priority

    @priority.setter
    def priority(self, priority):
        """Sets the priority of this WorkflowSummary.


        :param priority: The priority of this WorkflowSummary.  # noqa: E501
        :type: int
        """

        self._priority = priority

    @property
    def created_by(self):
        """Gets the created_by of this WorkflowSummary.  # noqa: E501


        :return: The created_by of this WorkflowSummary.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this WorkflowSummary.


        :param created_by: The created_by of this WorkflowSummary.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def output_size(self):
        """Gets the output_size of this WorkflowSummary.  # noqa: E501


        :return: The output_size of this WorkflowSummary.  # noqa: E501
        :rtype: int
        """
        return self._output_size

    @output_size.setter
    def output_size(self, output_size):
        """Sets the output_size of this WorkflowSummary.


        :param output_size: The output_size of this WorkflowSummary.  # noqa: E501
        :type: int
        """

        self._output_size = output_size

    @property
    def input_size(self):
        """Gets the input_size of this WorkflowSummary.  # noqa: E501


        :return: The input_size of this WorkflowSummary.  # noqa: E501
        :rtype: int
        """
        return self._input_size

    @input_size.setter
    def input_size(self, input_size):
        """Sets the input_size of this WorkflowSummary.


        :param input_size: The input_size of this WorkflowSummary.  # noqa: E501
        :type: int
        """

        self._input_size = input_size

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
        if issubclass(WorkflowSummary, dict):
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
        if not isinstance(other, WorkflowSummary):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
