import base64
import hashlib
import json
import secrets
from typing import Optional

import jsons
import pytest
import requests
from enochecker_core import (
    CheckerInfoMessage,
    CheckerMethod,
    CheckerResultMessage,
    CheckerTaskMessage,
    CheckerTaskResult,
)

global_round_id = 0
FLAG_REGEX_ASCII = r"ENO[A-Za-z0-9+\/=]{48}"
FLAG_REGEX_UTF8 = r"🥺[A-Za-z0-9+\/=]{48}🥺🥺"
REQUEST_TIMEOUT = 10
CHAIN_ID_PREFIX = secrets.token_hex(20)


@pytest.fixture
def checker_address(request):
    return request.config.getoption("--checker-address")


@pytest.fixture
def checker_port(request):
    return request.config.getoption("--checker-port")


@pytest.fixture
def service_address(request):
    return request.config.getoption("--service-address")


@pytest.fixture
def checker_url(checker_address, checker_port):
    return f"http://{checker_address}:{checker_port}"


def pytest_generate_tests(metafunc):
    flag_variants: int = metafunc.config.getoption("--flag-variants")
    noise_variants: int = metafunc.config.getoption("--noise-variants")
    havoc_variants: int = metafunc.config.getoption("--havoc-variants")
    exploit_variants: int = metafunc.config.getoption("--exploit-variants")

    if "flag_id" in metafunc.fixturenames:
        metafunc.parametrize("flag_id", range(flag_variants))
    if "flag_id_multiplied" in metafunc.fixturenames:
        metafunc.parametrize(
            "flag_id_multiplied", range(flag_variants, flag_variants * 2)
        )
    if "flag_variants" in metafunc.fixturenames:
        metafunc.parametrize("flag_variants", [flag_variants])

    if "noise_id" in metafunc.fixturenames:
        metafunc.parametrize("noise_id", range(noise_variants))
    if "noise_id_multiplied" in metafunc.fixturenames:
        metafunc.parametrize(
            "noise_id_multiplied", range(noise_variants, noise_variants * 2)
        )
    if "noise_variants" in metafunc.fixturenames:
        metafunc.parametrize("noise_variants", [noise_variants])

    if "havoc_id" in metafunc.fixturenames:
        metafunc.parametrize("havoc_id", range(havoc_variants))
    if "havoc_id_multiplied" in metafunc.fixturenames:
        metafunc.parametrize(
            "havoc_id_multiplied", range(havoc_variants, havoc_variants * 2)
        )
    if "havoc_variants" in metafunc.fixturenames:
        metafunc.parametrize("havoc_variants", [havoc_variants])

    if "exploit_id" in metafunc.fixturenames:
        metafunc.parametrize("exploit_id", range(exploit_variants))
    if "exploit_variants" in metafunc.fixturenames:
        metafunc.parametrize("exploit_variants", [exploit_variants])

    if "encoding" in metafunc.fixturenames:
        metafunc.parametrize("encoding", ["ascii", "utf8"])


def generate_dummyflag(encoding: str) -> str:
    if encoding == "utf8":
        flag = "🥺" + base64.b64encode(secrets.token_bytes(36)).decode() + "🥺🥺"
    else:
        flag = "ENO" + base64.b64encode(secrets.token_bytes(36)).decode()
    assert len(flag) == 51
    return flag


@pytest.fixture
def round_id():
    global global_round_id
    global_round_id += 1
    return global_round_id


def _flag_regex_for_encoding(encoding: str) -> str:
    if encoding == "utf8":
        return FLAG_REGEX_UTF8
    return FLAG_REGEX_ASCII


def _create_request_message(
    method: str,
    round_id: int,
    variant_id: int,
    service_address: str,
    flag: Optional[str] = None,
    unique_variant_index: Optional[int] = None,
    flag_regex: Optional[str] = None,
    flag_hash: Optional[str] = None,
    attack_info: Optional[str] = None,
) -> CheckerTaskMessage:
    if unique_variant_index is None:
        unique_variant_index = variant_id

    prefix = "havoc"
    if method in ("putflag", "getflag"):
        prefix = "flag"
    elif method in ("putnoise", "getnoise"):
        prefix = "noise"
    elif method == "exploit":
        prefix = "exploit"
    task_chain_id = (
        f"{CHAIN_ID_PREFIX}_{prefix}_s0_r{round_id}_t0_i{unique_variant_index}"
    )

    return CheckerTaskMessage(
        task_id=round_id,
        method=CheckerMethod(method),
        address=service_address,
        team_id=0,
        team_name="teamname",
        current_round_id=round_id,
        related_round_id=round_id,
        flag=flag,
        variant_id=variant_id,
        timeout=REQUEST_TIMEOUT * 1000,
        round_length=60000,
        task_chain_id=task_chain_id,
        flag_regex=flag_regex,
        flag_hash=flag_hash,
        attack_info=attack_info,
    )


def _jsonify_request_message(request_message: CheckerTaskMessage):
    return jsons.dumps(
        request_message,
        use_enum_name=False,
        key_transformer=jsons.KEY_TRANSFORMER_CAMELCASE,
        strict=True,
    )


def _test_putflag(
    flag,
    round_id,
    flag_id,
    service_address,
    checker_url,
    unique_variant_index=None,
    expected_result=CheckerTaskResult.OK,
) -> Optional[str]:
    if unique_variant_index is None:
        unique_variant_index = flag_id
    request_message = _create_request_message(
        "putflag",
        round_id,
        flag_id,
        service_address,
        flag,
        unique_variant_index=unique_variant_index,
    )
    msg = _jsonify_request_message(request_message)
    r = requests.post(
        f"{checker_url}",
        data=msg,
        headers={"content-type": "application/json"},
        timeout=REQUEST_TIMEOUT,
    )
    result_message: CheckerResultMessage = jsons.loads(
        r.content, CheckerResultMessage, key_transformer=jsons.KEY_TRANSFORMER_SNAKECASE
    )
    assert (
        CheckerTaskResult(result_message.result) == expected_result
    ), f"\nMessage: {result_message.message}\n"
    return result_message.attack_info


def _test_getflag(
    flag,
    round_id,
    flag_id,
    service_address,
    checker_url,
    unique_variant_index=None,
    expected_result=CheckerTaskResult.OK,
):
    if unique_variant_index is None:
        unique_variant_index = flag_id
    request_message = _create_request_message(
        "getflag",
        round_id,
        flag_id,
        service_address,
        flag,
        unique_variant_index=unique_variant_index,
    )
    msg = _jsonify_request_message(request_message)
    r = requests.post(
        f"{checker_url}",
        data=msg,
        headers={"content-type": "application/json"},
        timeout=REQUEST_TIMEOUT,
    )
    assert r.status_code == 200
    result_message: CheckerResultMessage = jsons.loads(
        r.content, CheckerResultMessage, key_transformer=jsons.KEY_TRANSFORMER_SNAKECASE
    )
    assert (
        CheckerTaskResult(result_message.result) == expected_result
    ), f"\nMessage: {result_message.message}\n"


def _test_putnoise(
    round_id,
    noise_id,
    service_address,
    checker_url,
    unique_variant_index=None,
    expected_result=CheckerTaskResult.OK,
):
    if unique_variant_index is None:
        unique_variant_index = noise_id
    request_message = _create_request_message(
        "putnoise",
        round_id,
        noise_id,
        service_address,
        unique_variant_index=unique_variant_index,
    )
    msg = _jsonify_request_message(request_message)
    r = requests.post(
        f"{checker_url}",
        data=msg,
        headers={"content-type": "application/json"},
        timeout=REQUEST_TIMEOUT,
    )
    assert r.status_code == 200
    result_message: CheckerResultMessage = jsons.loads(
        r.content, CheckerResultMessage, key_transformer=jsons.KEY_TRANSFORMER_SNAKECASE
    )
    assert (
        CheckerTaskResult(result_message.result) == expected_result
    ), f"\nMessage: {result_message.message}\n"


def _test_getnoise(
    round_id,
    noise_id,
    service_address,
    checker_url,
    unique_variant_index=None,
    expected_result=CheckerTaskResult.OK,
):
    if unique_variant_index is None:
        unique_variant_index = noise_id
    request_message = _create_request_message(
        "getnoise",
        round_id,
        noise_id,
        service_address,
        unique_variant_index=unique_variant_index,
    )
    msg = _jsonify_request_message(request_message)
    r = requests.post(
        f"{checker_url}",
        data=msg,
        headers={"content-type": "application/json"},
        timeout=REQUEST_TIMEOUT,
    )
    assert r.status_code == 200
    result_message: CheckerResultMessage = jsons.loads(
        r.content, CheckerResultMessage, key_transformer=jsons.KEY_TRANSFORMER_SNAKECASE
    )
    assert (
        CheckerTaskResult(result_message.result) == expected_result
    ), f"\nMessage: {result_message.message}\n"


def _test_havoc(
    round_id,
    havoc_id,
    service_address,
    checker_url,
    unique_variant_index=None,
    expected_result=CheckerTaskResult.OK,
):
    if unique_variant_index is None:
        unique_variant_index = havoc_id
    request_message = _create_request_message(
        "havoc",
        round_id,
        havoc_id,
        service_address,
        unique_variant_index=unique_variant_index,
    )
    msg = _jsonify_request_message(request_message)
    r = requests.post(
        f"{checker_url}",
        data=msg,
        headers={"content-type": "application/json"},
        timeout=REQUEST_TIMEOUT,
    )
    assert r.status_code == 200
    result_message: CheckerResultMessage = jsons.loads(
        r.content, CheckerResultMessage, key_transformer=jsons.KEY_TRANSFORMER_SNAKECASE
    )
    assert (
        CheckerTaskResult(result_message.result) == expected_result
    ), f"\nMessage: {result_message.message}\n"


def _test_exploit(
    flag_regex,
    flag_hash,
    attack_info,
    round_id,
    exploit_id,
    service_address,
    checker_url,
    unique_variant_index=None,
    expected_result=CheckerTaskResult.OK,
) -> Optional[str]:
    if unique_variant_index is None:
        unique_variant_index = exploit_id
    request_message = _create_request_message(
        "exploit",
        round_id,
        exploit_id,
        service_address,
        unique_variant_index=unique_variant_index,
        flag_regex=flag_regex,
        flag_hash=flag_hash,
        attack_info=attack_info,
    )
    msg = _jsonify_request_message(request_message)
    r = requests.post(
        f"{checker_url}",
        data=msg,
        headers={"content-type": "application/json"},
        timeout=REQUEST_TIMEOUT,
    )
    assert r.status_code == 200
    result_message: CheckerResultMessage = jsons.loads(
        r.content, CheckerResultMessage, key_transformer=jsons.KEY_TRANSFORMER_SNAKECASE
    )
    assert (
        CheckerTaskResult(result_message.result) == expected_result
    ), f"\nMessage: {result_message.message}\n"
    return result_message.flag


def test_putflag(encoding, round_id, flag_id, service_address, checker_url):
    flag = generate_dummyflag(encoding)
    _test_putflag(flag, round_id, flag_id, service_address, checker_url)


def test_putflag_multiplied(
    encoding, round_id, flag_id_multiplied, flag_variants, service_address, checker_url
):
    flag = generate_dummyflag(encoding)
    _test_putflag(
        flag,
        round_id,
        flag_id_multiplied % flag_variants,
        service_address,
        checker_url,
        unique_variant_index=flag_id_multiplied,
    )


def test_putflag_invalid_variant(
    encoding, round_id, flag_variants, service_address, checker_url
):
    flag = generate_dummyflag(encoding)
    _test_putflag(
        flag,
        round_id,
        flag_variants,
        service_address,
        checker_url,
        expected_result=CheckerTaskResult.INTERNAL_ERROR,
    )


def test_getflag(encoding, round_id, flag_id, service_address, checker_url):
    flag = generate_dummyflag(encoding)
    _test_putflag(flag, round_id, flag_id, service_address, checker_url)
    _test_getflag(flag, round_id, flag_id, service_address, checker_url)


def test_getflag_after_second_putflag_with_same_variant_id(
    encoding, round_id, flag_id, flag_variants, service_address, checker_url
):
    flag = generate_dummyflag(encoding)
    _test_putflag(flag, round_id, flag_id, service_address, checker_url)
    _test_putflag(
        generate_dummyflag(encoding),
        round_id,
        flag_id,
        service_address,
        checker_url,
        unique_variant_index=flag_id + flag_variants,
    )
    _test_getflag(flag, round_id, flag_id, service_address, checker_url)


def test_getflag_twice(encoding, round_id, flag_id, service_address, checker_url):
    flag = generate_dummyflag(encoding)
    _test_putflag(flag, round_id, flag_id, service_address, checker_url)
    _test_getflag(flag, round_id, flag_id, service_address, checker_url)
    _test_getflag(flag, round_id, flag_id, service_address, checker_url)


def test_getflag_wrong_flag(encoding, round_id, flag_id, service_address, checker_url):
    flag = generate_dummyflag(encoding)
    _test_putflag(flag, round_id, flag_id, service_address, checker_url)
    wrong_flag = generate_dummyflag(encoding)
    _test_getflag(
        wrong_flag,
        round_id,
        flag_id,
        service_address,
        checker_url,
        expected_result=CheckerTaskResult.MUMBLE,
    )


def test_getflag_without_putflag(
    encoding, round_id, flag_id, service_address, checker_url
):
    flag = generate_dummyflag(encoding)
    _test_getflag(
        flag,
        round_id,
        flag_id,
        service_address,
        checker_url,
        expected_result=CheckerTaskResult.MUMBLE,
    )


def test_getflag_multiplied(
    encoding, round_id, flag_id_multiplied, flag_variants, service_address, checker_url
):
    flag = generate_dummyflag(encoding)
    _test_putflag(
        flag,
        round_id,
        flag_id_multiplied % flag_variants,
        service_address,
        checker_url,
        unique_variant_index=flag_id_multiplied,
    )
    _test_getflag(
        flag,
        round_id,
        flag_id_multiplied % flag_variants,
        service_address,
        checker_url,
        unique_variant_index=flag_id_multiplied,
    )


def test_getflag_invalid_variant(
    encoding, round_id, flag_variants, service_address, checker_url
):
    flag = generate_dummyflag(encoding)
    _test_getflag(
        flag,
        round_id,
        flag_variants,
        service_address,
        checker_url,
        expected_result=CheckerTaskResult.INTERNAL_ERROR,
    )


def test_putnoise(round_id, noise_id, service_address, checker_url):
    _test_putnoise(round_id, noise_id, service_address, checker_url)


def test_putnoise_multiplied(
    round_id, noise_id_multiplied, noise_variants, service_address, checker_url
):
    _test_putnoise(
        round_id,
        noise_id_multiplied % noise_variants,
        service_address,
        checker_url,
        unique_variant_index=noise_id_multiplied,
    )


def test_putnoise_invalid_variant(
    round_id, noise_variants, service_address, checker_url
):
    _test_putnoise(
        round_id,
        noise_variants,
        service_address,
        checker_url,
        expected_result=CheckerTaskResult.INTERNAL_ERROR,
    )


def test_getnoise(round_id, noise_id, service_address, checker_url):
    _test_putnoise(round_id, noise_id, service_address, checker_url)
    _test_getnoise(round_id, noise_id, service_address, checker_url)


def test_getnoise_after_second_putnoise_with_same_variant_id(
    round_id, noise_id, noise_variants, service_address, checker_url
):
    _test_putnoise(round_id, noise_id, service_address, checker_url)
    _test_putnoise(
        round_id,
        noise_id,
        service_address,
        checker_url,
        unique_variant_index=noise_id + noise_variants,
    )
    _test_getnoise(round_id, noise_id, service_address, checker_url)


def test_getnoise_twice(round_id, noise_id, service_address, checker_url):
    _test_putnoise(round_id, noise_id, service_address, checker_url)
    _test_getnoise(round_id, noise_id, service_address, checker_url)
    _test_getnoise(round_id, noise_id, service_address, checker_url)


def test_getnoise_without_putnoise(round_id, noise_id, service_address, checker_url):
    _test_getnoise(
        round_id,
        noise_id,
        service_address,
        checker_url,
        expected_result=CheckerTaskResult.MUMBLE,
    )


def test_getnoise_multiplied(
    round_id, noise_id_multiplied, noise_variants, service_address, checker_url
):
    _test_putnoise(
        round_id,
        noise_id_multiplied % noise_variants,
        service_address,
        checker_url,
        unique_variant_index=noise_id_multiplied,
    )
    _test_getnoise(
        round_id,
        noise_id_multiplied % noise_variants,
        service_address,
        checker_url,
        unique_variant_index=noise_id_multiplied,
    )


def test_getnoise_invalid_variant(
    round_id, noise_variants, service_address, checker_url
):
    _test_getnoise(
        round_id,
        noise_variants,
        service_address,
        checker_url,
        expected_result=CheckerTaskResult.INTERNAL_ERROR,
    )


def test_havoc(round_id, havoc_id, service_address, checker_url):
    _test_havoc(round_id, havoc_id, service_address, checker_url)


def test_havoc_multiplied(
    round_id, havoc_id_multiplied, havoc_variants, service_address, checker_url
):
    _test_havoc(
        round_id,
        havoc_id_multiplied % havoc_variants,
        service_address,
        checker_url,
        unique_variant_index=havoc_id_multiplied,
    )


def test_havoc_invalid_variant(round_id, havoc_variants, service_address, checker_url):
    _test_havoc(
        round_id,
        havoc_variants,
        service_address,
        checker_url,
        expected_result=CheckerTaskResult.INTERNAL_ERROR,
    )


def _do_exploit_run(
    encoding, round_id, exploit_id, flag_id, service_address, checker_url
):
    try:
        flag = generate_dummyflag(encoding)
        flag_hash = hashlib.sha256(flag.encode()).hexdigest()

        attack_info = _test_putflag(
            flag, round_id, flag_id, service_address, checker_url
        )
        found_flag = _test_exploit(
            _flag_regex_for_encoding(encoding),
            flag_hash,
            attack_info,
            round_id,
            exploit_id,
            service_address,
            checker_url,
        )
        print(found_flag)
        if found_flag == flag:
            return True, None

        return False, Exception(f"Found flag is incorrect. Expected: {flag}. Found: {found_flag}")

    except Exception as e:
        return False, e


def test_exploit_per_exploit_id(
    encoding, round_id, exploit_id, flag_variants, service_address, checker_url
):
    results = [
        _do_exploit_run(
            encoding, round_id, exploit_id, flag_id, service_address, checker_url
        )
        for flag_id in range(flag_variants)
    ]
    if any(r[0] for r in results):
        return
    raise Exception([r[1] for r in results])


def test_exploit_per_flag_id(
    encoding, round_id, exploit_variants, flag_id, service_address, checker_url
):
    results = [
        _do_exploit_run(
            encoding, round_id, exploit_id, flag_id, service_address, checker_url
        )
        for exploit_id in range(exploit_variants)
    ]
    if any(r[0] for r in results):
        return
    raise Exception([r[1] for r in results])


def test_exploit_invalid_variant(
    encoding, round_id, exploit_variants, service_address, checker_url
):
    flag = generate_dummyflag(encoding)
    flag_hash = hashlib.sha256(flag.encode()).hexdigest()

    _test_exploit(
        _flag_regex_for_encoding(encoding),
        flag_hash,
        None,
        round_id,
        exploit_variants,
        service_address,
        checker_url,
        expected_result=CheckerTaskResult.INTERNAL_ERROR,
    )


def test_checker_info_message_case(
    checker_url,
):
    r = requests.get(
        f"{checker_url}/service",
        timeout=REQUEST_TIMEOUT,
    )
    assert r.status_code == 200
    result_message: CheckerInfoMessage = jsons.loads(
        r.content, CheckerInfoMessage, key_transformer=jsons.KEY_TRANSFORMER_SNAKECASE
    )
    assert r.json() == json.loads(
        jsons.dumps(result_message, key_transformer=jsons.KEY_TRANSFORMER_CAMELCASE)
    )
