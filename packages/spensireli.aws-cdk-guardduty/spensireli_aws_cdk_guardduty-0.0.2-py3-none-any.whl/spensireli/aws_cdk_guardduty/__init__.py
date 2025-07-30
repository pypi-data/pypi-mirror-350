r'''
# cdk-guardduty

[![codecov](https://codecov.io/gh/spensireli/cdk-guardduty/graph/badge.svg?token=YVFUKBJE93)](https://codecov.io/gh/spensireli/cdk-guardduty)

Enables GuardDuty and allows for enabling of all or some features.

By default

* GuardDuty Detector is Created
* GuardDuty Detector is Enabled
* Kubernetes Audit Log Monitoring is Enabled
* Malware Protection Monitoring is Enabled
* S3 Logs Monitoring is Enabled
* Runtime Monitoring is Enabled

## Example

### Default Enable All

```python
import { GuardDutyConstruct } from '@spensireli/cdk-guardduty';
new GuardDutyConstruct(stack, 'GuardDutyConstructTest');
```

### Choose Features to Enable

```python
import { GuardDutyConstruct } from '@spensireli/cdk-guardduty';
new GuardDutyConstruct(stack, 'GuardDutyConstructTest', {
    enableGuardDuty: true,
    kubernetesAuditLogs: true,
    malwareProtection: true,
    s3Logs: true,
  });
```
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ._jsii import *

import constructs as _constructs_77d1e7e8


class GuardDutyConstruct(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@spensireli/cdk-guardduty.GuardDutyConstruct",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        enable_guard_duty: typing.Optional[builtins.bool] = None,
        kubernetes_audit_logs: typing.Optional[builtins.bool] = None,
        malware_protection: typing.Optional[builtins.bool] = None,
        s3_logs: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param enable_guard_duty: 
        :param kubernetes_audit_logs: 
        :param malware_protection: 
        :param s3_logs: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91fd2dcd9029704701a47a31665a555bd9143fc10569122bd8f225300e2de9b3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GuardDutyConstructProps(
            enable_guard_duty=enable_guard_duty,
            kubernetes_audit_logs=kubernetes_audit_logs,
            malware_protection=malware_protection,
            s3_logs=s3_logs,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="detectorId")
    def detector_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "detectorId"))

    @detector_id.setter
    def detector_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da4f5bb0445ef11868c0559b8110a6799193df2af4eeff7109a98d5adc4b7c1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "detectorId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@spensireli/cdk-guardduty.GuardDutyConstructProps",
    jsii_struct_bases=[],
    name_mapping={
        "enable_guard_duty": "enableGuardDuty",
        "kubernetes_audit_logs": "kubernetesAuditLogs",
        "malware_protection": "malwareProtection",
        "s3_logs": "s3Logs",
    },
)
class GuardDutyConstructProps:
    def __init__(
        self,
        *,
        enable_guard_duty: typing.Optional[builtins.bool] = None,
        kubernetes_audit_logs: typing.Optional[builtins.bool] = None,
        malware_protection: typing.Optional[builtins.bool] = None,
        s3_logs: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param enable_guard_duty: 
        :param kubernetes_audit_logs: 
        :param malware_protection: 
        :param s3_logs: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a41dbb1d03848fb0f40534289c76df89345422f83eea125d2963b1a31ebdb616)
            check_type(argname="argument enable_guard_duty", value=enable_guard_duty, expected_type=type_hints["enable_guard_duty"])
            check_type(argname="argument kubernetes_audit_logs", value=kubernetes_audit_logs, expected_type=type_hints["kubernetes_audit_logs"])
            check_type(argname="argument malware_protection", value=malware_protection, expected_type=type_hints["malware_protection"])
            check_type(argname="argument s3_logs", value=s3_logs, expected_type=type_hints["s3_logs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_guard_duty is not None:
            self._values["enable_guard_duty"] = enable_guard_duty
        if kubernetes_audit_logs is not None:
            self._values["kubernetes_audit_logs"] = kubernetes_audit_logs
        if malware_protection is not None:
            self._values["malware_protection"] = malware_protection
        if s3_logs is not None:
            self._values["s3_logs"] = s3_logs

    @builtins.property
    def enable_guard_duty(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("enable_guard_duty")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def kubernetes_audit_logs(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("kubernetes_audit_logs")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def malware_protection(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("malware_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def s3_logs(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("s3_logs")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GuardDutyConstructProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "GuardDutyConstruct",
    "GuardDutyConstructProps",
]

publication.publish()

def _typecheckingstub__91fd2dcd9029704701a47a31665a555bd9143fc10569122bd8f225300e2de9b3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    enable_guard_duty: typing.Optional[builtins.bool] = None,
    kubernetes_audit_logs: typing.Optional[builtins.bool] = None,
    malware_protection: typing.Optional[builtins.bool] = None,
    s3_logs: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da4f5bb0445ef11868c0559b8110a6799193df2af4eeff7109a98d5adc4b7c1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a41dbb1d03848fb0f40534289c76df89345422f83eea125d2963b1a31ebdb616(
    *,
    enable_guard_duty: typing.Optional[builtins.bool] = None,
    kubernetes_audit_logs: typing.Optional[builtins.bool] = None,
    malware_protection: typing.Optional[builtins.bool] = None,
    s3_logs: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass
