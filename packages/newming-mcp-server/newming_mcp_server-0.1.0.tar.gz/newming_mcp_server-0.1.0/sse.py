# =========================
# MCP 서버 실행/개발 환경 안내 (for Cursor)
# =========================
# 1. .env 또는 환경변수로 username, password, license를 반드시 지정해야 합니다.
#    (예: export username=...; export password=...; export license=...)
# 2. MCP 서버 실행: python sse.py
# 3. requirements.txt에 fastmcp, pandas, requests 등 필수 패키지 포함 필요
# 4. Cursor에서 MCP 플러그인/확장 기능을 사용할 때, 이 서버를 sse 모드로 실행하면 연동됩니다.
# 5. (예시) requirements.txt 내용:
#    fastmcp
#    pandas
#    requests
# 6. (옵션) .env 파일을 루트에 두고 dotenv로 환경변수 자동 로드 가능
# 7. API 문서 : https://recommend.griplabs.io/swagger-ui/index.html
# =========================

import os
import datetime
import argparse
import sys
import json
import requests
import shutil
from mcp.server.fastmcp import FastMCP

mcp = FastMCP()

# 컨피그 정보 로드
def load_environment_config():
    config = {
        "license": os.getenv("license")
    }
    
    if not config["license"]:
        raise ValueError("필수 설정값이 누락되었습니다. (license 필요)")
        
    return config

# 도구 호출 로깅
def log_tool_call(tool_name, params, result=None):
    return
    # log_dir = "logs"
    # os.makedirs(log_dir, exist_ok=True)
    # today = datetime.datetime.now().strftime("%Y-%m-%d")
    # log_path = os.path.join(log_dir, "tool_access.log")
    # # 파일이 존재하면, 마지막 수정 날짜 확인
    # if os.path.exists(log_path):
    #     mtime = datetime.datetime.fromtimestamp(os.path.getmtime(log_path)).strftime("%Y-%m-%d")
    #     if mtime != today:
    #         # 날짜가 바뀌었으면 백업
    #         backup_path = os.path.join(log_dir, f"tool_access_{mtime}.log")
    #         shutil.move(log_path, backup_path)
    # now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # log_line = f"[{now}] {tool_name} called with params: {params}"
    # if result is not None:
    #     result_str = str(result)
    #     log_line += f" | return: {result_str}"
    # with open(log_path, "a", encoding="utf-8") as f:
    #     f.write(log_line + "\n")

@mcp.tool()
def get_location_by_ip() -> str:
    """
    IP 기반으로 현재 위치(도시, 지역, 국가, 위도/경도, 상세 주소)를 반환합니다.
    상세 주소는 OpenStreetMap Nominatim 무료 API를 사용해 위도/경도 기준으로 역지오코딩합니다.
    (단, Nominatim 쿼터 제한: 1초 1회)
    """
    config = load_environment_config()
    log_tool_call("get_location_by_ip", {})
    try:
        url = "https://ipinfo.io/json"
        response = requests.get(url)
        if response.status_code != 200:
            result = f"Error: 위치 정보를 가져올 수 없습니다. (HTTP {response.status_code})"
            log_tool_call("get_location_by_ip", {}, result)
            return result
        data = response.json()
        city = data.get("city", "알 수 없음")
        region = data.get("region", "알 수 없음")
        country = data.get("country", "알 수 없음")
        loc = data.get("loc", "알 수 없음")
        # 위도/경도 분리
        if loc != "알 수 없음" and "," in loc:
            lat, lon = loc.split(",")
            # Nominatim 역지오코딩
            try:
                nominatim_url = "https://nominatim.openstreetmap.org/reverse"
                params = {
                    "lat": lat,
                    "lon": lon,
                    "format": "json"
                }
                headers = {"User-Agent": "newming-mcp-server/1.0"}
                nom_response = requests.get(nominatim_url, params=params, headers=headers, timeout=5)
                if nom_response.status_code == 200:
                    nom_data = nom_response.json()
                    address = nom_data.get("display_name", "상세 주소를 찾을 수 없습니다.")
                else:
                    address = f"상세 주소 조회 오류: HTTP {nom_response.status_code}"
            except Exception as e:
                address = f"상세 주소 조회 중 오류: {e}"
        else:
            address = "상세 주소를 찾을 수 없습니다."
        result = f"현재 위치: {address} (위도/경도: {loc})"
        log_tool_call("get_location_by_ip", {}, result)
        return result
    except Exception as e:
        result = f"Error: {e}"
        log_tool_call("get_location_by_ip", {}, result)
        return result

@mcp.tool()
def festival_search_api() -> str:
    """
    대한민국 축제 데이터를 외부 API(https://recommend.griplabs.io/api/v1/festival/all-festival-survey)에서 실시간으로 받아 원본 JSON만 반환합니다.
    각 행은 dict로 변환되어 포함됩니다.

    [주요 활용/요구사항]
    ① 축제 데이터 조회: 사용자가 특정 지역이나 시기의 축제 정보를 요청하면 AI가 관련 데이터를 추출해 제공
    ② 맞춤형 분석 제공: 지자체나 기업이 원하는 조건에 맞는 축제 분석 데이터를 자동 생성
    ③ 트렌드 예측: 과거 데이터를 기반으로 향후 축제 트렌드나 방문객 수 예측

    [다른 도구와 조합 활용 예시]
    - festival_awareness_api, festival_visitor_spending_range_api 등과 함께 사용하면, 만족도/방문객 특성/인지도 등 다양한 조건으로 종합 분석이 가능합니다.
    - 예: "SNS 인지도가 높고, 가족 방문 비율이 높은 축제만 뽑아줘" → 여러 도구 결과를 조합해 안내

    [LLM 가이드]
    - 사용자의 질문 의도(조회/분석/예측)에 따라 적절한 MCP 도구를 조합해서 사용하세요.
    - 여러 도구 결과를 합쳐서 표, 그래프, 자연어로 종합 안내하세요.

    [주요 필드]
      - id: 고유 식별자
      - festivalIdentifier: 축제명
      - provinceCity: 시도
      - districtBasicGov: 시군구
      - festivalType: 축제 유형
      - eventPeriod: 개최기간
      - overallSatisfaction: 전반적 만족도(점수)
      - revisitIntention: 재방문 의향(점수)
      - recommendIntention: 타인 추천 의향(점수)
      - themeContentEmpathy: 축제 주제/내용 공감(점수)
      - festivalUsefulness: 축제 유익성(점수)
      - varietyOfAttractions: 다양한 볼거리(점수)
      - regionalImageImprovement: 지역 이미지 향상(점수)
      - communityNecessity: 지역사회 필요(점수)
      - desireForContinuation: 지속 개최희망(점수)
      - publicTransportAccess: 대중교통 접근성(점수)
      - parkingConvenience: 주차장 편리(점수)
      - sanitaryFacilities: 위생시설(점수)
      - safetyPreparedness: 안전사고 대비(점수)
      - expenseAppropriateness: 지출 비용 적정(점수)
      - festivalSitePrices: 축제장 물가(점수)
      - accommodationCosts: 숙박비(점수)
      - transportationCosts: 교통비(점수)
      - nearbyAmenityPrices: 주변 음식점/관광지 물가(점수)
      - nonLocalVisitorBPeriodAvg: 외지인 방문자(축제기간 평균)
      - localVisitorAPeriodAvg: 현지인 방문자(축제기간 평균)
      - totalVisitorPeriodAvg: 전체 방문자(축제기간 평균)
      - createdAt, updatedAt: 데이터 생성/수정일 등
    """
    import requests
    import os
    license_key = os.getenv("license")
    if not license_key:
        result = "API 호출용 라이센스(license) 환경변수가 설정되어 있지 않습니다."
        log_tool_call("festival_search_api", {}, result)
        return result
    url = "https://recommend.griplabs.io/api/v1/festival/all-festival-survey"
    headers = {"x-api-key": license_key}
    log_tool_call("festival_search_api", {})
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            result = f"API 호출 실패: HTTP {response.status_code} - {response.text}"
            log_tool_call("festival_search_api", {}, result)
            return result
        result_json = response.text
        log_tool_call("festival_search_api", {}, result_json)
        return result_json + "출처: 뉴밍"
    except Exception as e:
        result = f"API 호출 중 오류 발생: {e}"
        log_tool_call("festival_search_api", {}, result)
        return result

@mcp.tool()
def festival_visitor_spending_range_api() -> str:
    """
    대한민국 축제별 방문객 지출 구간(금액대별 비율) 데이터를 실시간으로 받아 원본 JSON만 반환합니다.
    API: https://recommend.griplabs.io/api/v1/festival/all-visitor-spending-range

    [주요 활용/요구사항]
    ① 축제별 방문객 소비 패턴 분석
    ② 맞춤형 분석 제공: 예) 10만원 미만 지출 비율이 높은 축제만 추출
    ③ 트렌드 예측: 연도별 지출 변화 등

    [다른 도구와 조합 활용 예시]
    - festival_search_api, festival_awareness_api 등과 함께 사용하면, 만족도+지출+인지도 등 종합 분석이 가능합니다.
    - 예: "지출이 10만원 미만인 축제만, 만족도 순으로 TOP5 뽑아줘"

    [LLM 가이드]
    - 여러 도구 결과를 합쳐서 표, 그래프, 자연어로 안내하세요.

    [주요 필드]
    - id: 고유 식별자
    - festivalIdentifier: 축제명
    - spentNothing: 지출 없음(%)
    - spentUnder50kKrw: 5만원 미만 지출(%)
    - spent50kToUnder100kKrw: 5만원~10만원 미만 지출(%)
    - spent100kToUnder150kKrw: 10만원~15만원 미만 지출(%)
    - spent150kToUnder200kKrw: 15만원~20만원 미만 지출(%)
    - spent200kToUnder300kKrw: 20만원~30만원 미만 지출(%)
    - spent300kToUnder500kKrw: 30만원~50만원 미만 지출(%)
    - spent500kKrwOrMore: 50만원 이상 지출(%)
    - createdAt, updatedAt: 데이터 생성/수정일 등
    """
    import requests, os
    license_key = os.getenv("license")
    if not license_key:
        return "API 호출용 라이센스(license) 환경변수가 설정되어 있지 않습니다."
    url = "https://recommend.griplabs.io/api/v1/festival/all-visitor-spending-range"
    headers = {"x-api-key": license_key}
    response = requests.get(url, headers=headers, timeout=10)
    return response.text if response.status_code == 200 else f"API 호출 실패: HTTP {response.status_code} - {response.text}" + "출처: 뉴밍"

@mcp.tool()
def festival_visitor_composition_api() -> str:
    """
    대한민국 축제별 방문객 동행 유형(구성) 데이터를 실시간으로 받아 원본 JSON만 반환합니다.
    API: https://recommend.griplabs.io/api/v1/festival/all-visitor-composition

    [주요 활용/요구사항]
    ① 방문객 특성(가족, 친구 등) 분석
    ② 맞춤형 분석 제공: 예) 가족 방문 비율이 높은 축제만 추출
    ③ 트렌드 예측: 동행 유형 변화 등

    [다른 도구와 조합 활용 예시]
    - festival_search_api, festival_awareness_api 등과 함께 사용하면, 방문객 특성+만족도+인지도 등 종합 분석이 가능합니다.
    - 예: "가족 방문 비율이 높고, SNS 인지도가 높은 축제만 뽑아줘"

    [LLM 가이드]
    - 여러 도구 결과를 합쳐서 안내하세요.

    [주요 필드]
    - id: 고유 식별자
    - festivalIdentifier: 축제명
    - alone: 혼자 방문 비율(%)
    - friendsOrPartners: 친구/연인과 방문 비율(%)
    - familyOrRelatives: 가족/친척과 방문 비율(%)
    - organizedGroupOrMeeting: 단체/모임 방문 비율(%)
    - otherCompanionType: 기타 동행 유형 비율(%)
    - createdAt, updatedAt: 데이터 생성/수정일 등
    """
    import requests, os
    license_key = os.getenv("license")
    if not license_key:
        return "API 호출용 라이센스(license) 환경변수가 설정되어 있지 않습니다."
    url = "https://recommend.griplabs.io/api/v1/festival/all-visitor-composition"
    headers = {"x-api-key": license_key}
    response = requests.get(url, headers=headers, timeout=10)
    return response.text if response.status_code == 200 else f"API 호출 실패: HTTP {response.status_code} - {response.text}" + "출처: 뉴밍"

@mcp.tool()
def festival_nearby_tourism_activity_api() -> str:
    """
    대한민국 축제별 방문객의 인근 관광/여가 활동 데이터를 실시간으로 받아 원본 JSON만 반환합니다.
    API: https://recommend.griplabs.io/api/v1/festival/all-nearby-tourism-activity

    [주요 활용/요구사항]
    ① 축제 방문객의 관광/여가 활동 분석
    ② 맞춤형 분석 제공: 예) 음식점/카페 방문 비율이 높은 축제만 추출
    ③ 트렌드 예측: 관광/여가 활동 변화 등

    [다른 도구와 조합 활용 예시]
    - festival_search_api, festival_visitor_composition_api 등과 함께 사용하면, 관광/여가+방문객 특성+만족도 등 종합 분석이 가능합니다.
    - 예: "음식점/카페 방문 비율이 높고, 가족 방문 비율이 높은 축제만 뽑아줘"

    [LLM 가이드]
    - 여러 도구 결과를 합쳐서 안내하세요.

    [주요 필드]
    - id: 고유 식별자
    - festivalIdentifier: 축제명
    - visitedAttractionsHeritageNature: 관광지/유적/자연 방문 비율(%)
    - visitedRestaurantsOrCafes: 음식점/카페 방문 비율(%)
    - visitedCulturalFacilitiesMuseumsExhibitions: 문화시설/박물관/전시 방문 비율(%)
    - visitedShoppingMallsOrOutlets: 쇼핑몰/아울렛 방문 비율(%)
    - visitedFestivalOnly: 축제만 방문한 비율(%)
    - createdAt, updatedAt: 데이터 생성/수정일 등
    """
    import requests, os
    license_key = os.getenv("license")
    if not license_key:
        return "API 호출용 라이센스(license) 환경변수가 설정되어 있지 않습니다."
    url = "https://recommend.griplabs.io/api/v1/festival/all-nearby-tourism-activity"
    headers = {"x-api-key": license_key}
    response = requests.get(url, headers=headers, timeout=10)
    return response.text if response.status_code == 200 else f"API 호출 실패: HTTP {response.status_code} - {response.text}" + "출처: 뉴밍"

@mcp.tool()
def festival_nearby_activity_region_api() -> str:
    """
    대한민국 축제별 방문객의 인근 활동 지역(축제 지역/인접 지역) 데이터를 실시간으로 받아 원본 JSON만 반환합니다.
    API: https://recommend.griplabs.io/api/v1/festival/all-nearby-activity-region

    [주요 활용/요구사항]
    ① 방문객의 활동 지역 분포 분석
    ② 맞춤형 분석 제공: 예) 축제 지역 내 활동 비율이 높은 축제만 추출
    ③ 트렌드 예측: 활동 지역 변화 등

    [다른 도구와 조합 활용 예시]
    - festival_search_api, festival_visitor_composition_api 등과 함께 사용하면, 활동 지역+방문객 특성+만족도 등 종합 분석이 가능합니다.
    - 예: "축제 지역 내 활동 비율이 높고, 가족 방문 비율이 높은 축제만 뽑아줘"

    [LLM 가이드]
    - 여러 도구 결과를 합쳐서 안내하세요.

    [주요 필드]
    - id: 고유 식별자
    - festivalIdentifier: 축제명
    - activitiesInFestivalRegion: 축제 지역 내 활동 비율(%)
    - activitiesInAdjacentRegion: 인접 지역 내 활동 비율(%)
    - createdAt, updatedAt: 데이터 생성/수정일 등
    """
    import requests, os
    license_key = os.getenv("license")
    if not license_key:
        return "API 호출용 라이센스(license) 환경변수가 설정되어 있지 않습니다."
    url = "https://recommend.griplabs.io/api/v1/festival/all-nearby-activity-region"
    headers = {"x-api-key": license_key}
    response = requests.get(url, headers=headers, timeout=10)
    return response.text if response.status_code == 200 else f"API 호출 실패: HTTP {response.status_code} - {response.text}" + "출처: 뉴밍"

@mcp.tool()
def festival_awareness_api() -> str:
    """
    대한민국 축제별 인지도(정보 획득 경로 등) 데이터를 실시간으로 받아 원본 JSON만 반환합니다.
    API: https://recommend.griplabs.io/api/v1/festival/all-festival-awareness

    [주요 활용/요구사항]
    ① 축제 인지도/정보 획득 경로 분석
    ② 맞춤형 분석 제공: 예) SNS 인지도가 높은 축제만 추출
    ③ 트렌드 예측: 인지도 변화 추이 분석 등

    [다른 도구와 조합 활용 예시]
    - festival_search_api, festival_visitor_composition_api 등과 함께 사용하면, 인지도+만족도+방문객 특성 등 종합 분석이 가능합니다.
    - 예: "SNS 인지도가 높고, 가족 방문 비율이 높은 축제만 표로 보여줘"

    [LLM 가이드]
    - 사용자의 질문 의도에 따라 여러 도구를 조합해 결과를 안내하세요.

    [주요 필드]
    - id: 고유 식별자
    - festivalIdentifier: 축제명
    - pressMediaArticlesNews: 언론/뉴스 기사 비율(%)
    - socialMediaSns: SNS/소셜미디어 비율(%)
    - offlineAdsBannersPamphlets: 오프라인 광고/현수막/팸플릿 비율(%)
    - localFestivalWebsite: 축제 공식 홈페이지 비율(%)
    - wordOfMouthFamilyFriends: 가족/지인 추천(구전) 비율(%)
    - pastPersonalVisitExperience: 과거 본인 방문 경험 비율(%)
    - accidentalVisitNoPriorInfo: 사전 정보 없이 우연히 방문 비율(%)
    - otherChannel: 기타 경로 비율(%)
    - createdAt, updatedAt: 데이터 생성/수정일 등
    """
    import requests, os
    license_key = os.getenv("license")
    if not license_key:
        return "API 호출용 라이센스(license) 환경변수가 설정되어 있지 않습니다."
    url = "https://recommend.griplabs.io/api/v1/festival/all-festival-awareness"
    headers = {"x-api-key": license_key}
    response = requests.get(url, headers=headers, timeout=10)
    return response.text if response.status_code == 200 else f"API 호출 실패: HTTP {response.status_code} - {response.text}" + "출처: 뉴밍"

# 명령줄 인자 파싱 및 환경 변수 설정
def parse_args_and_set_env():
    parser = argparse.ArgumentParser()
    parser.add_argument("--license", type=str, help="라이센스 키")
    args, _ = parser.parse_known_args()
    if args.license:
        os.environ["license"] = args.license
    return args

def main():
    args = parse_args_and_set_env()
    try:
        print("Starting MCP server...", file=sys.stderr)
        print(f"License key: {os.getenv('license')}", file=sys.stderr)
        mcp.run(transport="stdio")
    except Exception as e:
        print(f"[MCP SERVER ERROR] {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)

if __name__ == "__main__":
    main() 