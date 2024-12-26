import pprint
import re  # noqa: F401

import six


class SkipTaskRequest(object):
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
        "task_input": "dict(str, object)",
        "task_output": "dict(str, object)",
    }

    attribute_map = {"task_input": "taskInput", "task_output": "taskOutput"}

    def __init__(self, task_input=None, task_output=None):  # noqa: E501
        """SkipTaskRequest - a model defined in Swagger"""  # noqa: E501
        self._task_input = None
        self._task_output = None
        self.discriminator = None
        if task_input is not None:
            self.task_input = task_input
        if task_output is not None:
            self.task_output = task_output

    @property
    def task_input(self):
        """Gets the task_input of this SkipTaskRequest.  # noqa: E501


        :return: The task_input of this SkipTaskRequest.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._task_input

    @task_input.setter
    def task_input(self, task_input):
        """Sets the task_input of this SkipTaskRequest.


        :param task_input: The task_input of this SkipTaskRequest.  # noqa: E501
        :type: dict(str, object)
        """

        self._task_input = task_input

    @property
    def task_output(self):
        """Gets the task_output of this SkipTaskRequest.  # noqa: E501


        :return: The task_output of this SkipTaskRequest.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._task_output

    @task_output.setter
    def task_output(self, task_output):
        """Sets the task_output of this SkipTaskRequest.


        :param task_output: The task_output of this SkipTaskRequest.  # noqa: E501
        :type: dict(str, object)
        """

        self._task_output = task_output

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
        if issubclass(SkipTaskRequest, dict):
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
        if not isinstance(other, SkipTaskRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
