import re
from typing import Generator
from state_of_the_art.register_papers.website_content_extractor import WebsiteContentExtractor
from state_of_the_art.tables.article_translation_table import ArticleTranslationTable
from state_of_the_art.utils.llm.llm import LLM

def cleanup_content(content: str, min_words_to_keep: int = 1) -> str:
    # delete rows with less than n words
    # remove more than 2 sequential empty lines
    content = re.sub(r'\n\n\n+', '\n\n', content)

    content = "\n".join([line for line in content.splitlines() if len(line.split()) > min_words_to_keep or not line.strip()])
    return content


class SiteSpecificConfig:
    DER_SPIEGEL_COOKIE_STRING = """_sp_su=false; consentUUID=977b2bd0-aa94-4b4a-9105-ac06ffb1c0f7_38; consentDate=2024-11-16T19:49:54.258Z; _gcl_au=1.1.207139578.1731786595; AMCV_41833DF75A550B4B0A495DA6%40AdobeOrg=MCMID|73578940710808427093624698508056709066; _tt_enable_cookie=1; _ttp=5xATMCunmOqU5W8WAyT-RfQSGps.tt.1; kndctr_41833DF75A550B4B0A495DA6_AdobeOrg_iab_persist=%2D1138775289045451451; kndctr_41833DF75A550B4B0A495DA6_AdobeOrg_consent=general%3Din; _sharedid=32a65bb6-3467-4fa9-a4ec-6cc39a0c5d6c; _sharedid_cst=%2FiwmLG4s2w%3D%3D; xdefcc=G4b38db5e3499577a163859219a7a7e47f; _pbjs_userid_consent_data=594477825788978; sara_target_dpg=pw%3Dtrue%3Ajul2024; emqsegs=e0; adp_segs=e0; gdpr=1; euconsent-v2=CQILsUAQILsUAAGABCENBOFgAP_gAAPAAAYgJegR5CpFTWFCYXhRQONgGIQU0cAAAEQABACBAiABABMQYAQA02EyMASABAACAAAAIBABAAAECAAEAEAAAAAEAACAAAAAgAAIIAAAABEAQAIAAAoIAAAAAAAIAAABAAAAmAiACILAAECAAAAACAAAACAAAIAAAgAAAAAAAAAAAAAAAAAAAAAgAAIAAAAAARAAAQAAAAAAAABAIGWQBAB3AEIAYIAywAwJAdAAWABUADgAIIAZABoADwAIgATAA3gB-AEIAIYAYYAygB3AD2gH4AfoBFACNQEiASUAxQBuADiAKHAUeAvMBmYDVwG6hAA4AJAAjgEcAJSAlYBf4DIR0CMABYAFQAOAAggBkAGgAPAAiABMgC4ALoAYgA3gB-AEMAMMAZQA0QB3AD2gH4AfsBFAEWgI6AkoBigDcAHEAReAmQBQ4CjwF5gMsAZmA1cBuoDiwJaDgBAAFwASABHAI4ASkBKwC_wGQkIBAACwAuABiADeAO4AigBKQDFEAAIBHCUA0ABYAHAAeABEACYAFwAMQAhgB-AGKAReAo8BeZIAKABcAI4BHAErAL_KQGQAFgAVAA4ACCAGQAaAA8ACIAEwAKQAYgA_ACGAGUANGAfgB-gEWgI6AkoBigDcAIvAUOAvMBlgDdQIclAA4ACgALgAkACOAFsAjgBKS0AIAdwChywAUAFQApACOAHoAZmA.YAAAAAAAAAAA; kndctr_41833DF75A550B4B0A495DA6_AdobeOrg_identity=CiY3MzU3ODk0MDcxMDgwODQyNzA5MzYyNDY5ODUwODA1NjcwOTA2NlIRCJWymbSzMhgBKgRJUkwxMAGgAYGs4Ku%5FMvAB%5FKvgq78y; fonce_current_user=1; sara_user_session=active; sara_day=true; sara_user_session-id=ps%3A1735036959361.c26jj4u5; kndctr_79655FCF5C1D42160A495E15_AdobeOrg_cluster=irl1; kndctr_41833DF75A550B4B0A495DA6_AdobeOrg_cluster=irl1; xdefccpm=no; dicbo_id=%7B%22dicbo_fetch%22%3A1735036959982%7D; sara_gpv_page=sp.www%20%3E%20presentation%20%3E%203ce2cb38-beda-4b96-8012-b68486d83b6d; iqaa_gpv=https://www.spiegel.de/panorama/gesellschaft/katholische-kirche-muenster-warum-ex-priester-thomas-laufmoeller-sein-amt-zurueckgab-a-3ce2cb38-beda-4b96-8012-b68486d83b6d; accessInfo=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOnsiU3BnZSI6dHJ1ZSwiU3BtZXRlcmVkIjpmYWxzZSwiU3BwbHVzIjp0cnVlLCJTcHByaW50IjpmYWxzZSwiU3BwdXIiOmZhbHNlfSwiYWNjZXNzVG9rZW4iOiJMVHlPd0x1TjdtYkc5TG1rRXBWZlJ3bU5RZ0FpaWk1VTJ0TlYwRDJsMWRwV1hmdXpVNWxKWkROOWtTaWt4cHNTIiwidHJhY2tpbmdJZFNzbyI6Ijc1RDdENDI2MDBCRDQ1RTU4OTA2OUJCRkRCMzYxRjYyIiwiaWQ1SGFzaCI6IjVmNjVmMjA4NWNkZjk0OTE2MmEwODQ1NTFmN2RkMDM2Y2M5MDYxYTA3OTY1NTY3YmY0ZjM5ZDY0ZDJmODQyYmEiLCJoYXNoZWRCb0lkIjoiYTRiYWQ5ZWUxNTY0ODhhZWM4MThiZWQ0NTZlZDRhZjFjNmJmMDgyZjE5MmY1Y2VmZWIzODFlNmVmMzIzZjNkOSIsInJldmFsaWRhdGVBdCI6IjIwMjQtMTItMjRUMjM6NDU6MjYuMjk2OTIxOTk5KzAxOjAwIiwic2Vzc2lvbkxpbWl0IjoyLCJzZWNyZXRib3hLZXkiOiJkeCtlSzlxc3JFdjhCWERQd2JkcTBUNmg2VVdCcVhpdThPeTI4SjVzRGx3PSJ9.GTb8Bf7kugNPLTh4903Y3pMGi-iQp1idEx-BvfYMsKM; userInfo=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IkF1UWFacDUyWHVad1RFbHl1UTVpY09OZC0yX1pmbTVMeFFRUERwVmt5eTQ9IiwidXNlcm5hbWUiOiJwaHVSMS9KUUtzL0t1dG4xc3VNQjJrRUJqYWd4dThlUmRLZS9pN1V5RUF5S015K0ZBU3lLdE5WK2tjWlVOUFh4em1SVUwrSmtidms9IiwiZW1haWwiOiJucmorVzk4RXZoWWp0QmpBVHpBeEZ2VHFIWXg5QkI2bjR5RHZxTUpLMmY5VnV6a01VOTdGWTZlc2h5WStza05EMHJsMlFrdWJqM1pid09NMDVzSUNHZndmRlhXQ0VnPT0iLCJmaXJzdG5hbWUiOiJ0cDcxQTJiSytjcEVSZmNXdkN3U3BzSDZvNnEvU05meXBPbUcyczhtNlFSMHRxYUYrWk1PRDdMVUJFbkplaE09IiwibGFzdG5hbWUiOiJTZ0JDVWJFTUh5R1M1M3dscWhLZ1kwWFZRbkFoUEFLSTFpejVPZUt2WC94SDl2dGVRaEFXQUpUSFVXT0RpRW1JIiwibG9nb3JhRGF0YSI6ImV5SmhiR2NpT2lKU1UwRXRUMEZGVUNJc0ltVnVZeUk2SWtFeE1qaEhRMDBpZlEuSFg5VkZTbTJGaWFxRDd6S0M3WURDRUhwWW5pS0c5SmZYalpKdTFXdi1KTjlNai1hb3N3WHFZT2VFV3daNjNqajFrNzZPY3ZMbFJTRUIzbHdXUzdrZWVYWjhkbVRJQ3JRV0ZLTGh4YWNTeVBKMGQ5TkhtMmV6RjFCajU3VV80RWtGRDIwV2U0bnNyUFpYams3ei1ZSHF0bHVWaUxDdnkwVWY1N081Y1RrX0dSR21VWjNlOFFpLUFreGl5ZzJGU09CRzh6OWtRamxxSXMyNFJtd3ZQdGlBVmlwWEw3Zzc0UjBDNlZrYnJtemhBV3o1bnBhSUlxZWtZZ0RGYllnYnFIQnRfV055NUFHOWxSMkk4VVRWMlNEaWNnSVRZc3F3N0NQN1p2eEhlRmI5cEFuY3FLRnpGWTNuODNSa3o3ZTBHekxjN1JqREpQQnRoMmF2dTVtRnQwakJBLkxHOXdURHB2SW15X09iV0EuNDByZUVNZlJKa0NRelV3MGRQVEh2dGc5TS1DYWZNUDdKck1hSzFORDN2T1RPSXkxRnhvSG5fSGhwdHdmRVc3bW5ub0pGMkpicWk1NzUtcl80TjA3XzNwZHZGRkpxZldSY0ZPX2FlM3RZMEgxTFFpcVZMcDYycVJDbjVnQ1VuS2FXVnBPSGw5VjBBUGozUVRlUlZGM2ZudHpfV0M3ZEFQaUVuUWZtVlppRkIxLVcycmNxVUI5UFJ1b0NqLTlKU1pTOGRqR21RLlRpOUVscmFLaWh5OUZFUjg5V0kyVnciLCJhdWQiOiJUQUxLX1RPS0VOX0FVRElFTkNFIiwiZXhwIjoxNzM1MDgwMzI2LCJpc3MiOiJodHRwczovL3Byb2QudGFsay5zcGllZ2VsLmRlIiwic3ViIjoiQXVRYVpwNTJYdVp3VEVseXVRNWljT05kLTJfWmZtNUx4UVFQRHBWa3l5ND0ifQ.NH1ILupXv-3Pc333BwguHbzirhf51raz4J4HQ8pkmjo; __gads=ID=ba22fcae2d1c49c6:T=1734990109:RT=1735037127:S=ALNI_MYny2zZXcX3A6hoHImWSaml5EM2Yw; __gpi=UID=00000f7abf4a82fe:T=1734990109:RT=1735037127:S=ALNI_MYAadRVYYjlk0CHWV-BC71_0wNNWw; __eoi=ID=f7e451814bd33ff1:T=1734990109:RT=1735037127:S=AA-AfjYQxl6ERxqhMOgq0FhQfBT8; cto_bidid=tCdqs193am5YWFpLQ1hZT0FXdkM0NGdZQ3JNMFYzWDBQWERXMkl5MzNJY2tJb0tWTjlUOGprWWVXOThrVk1mVkNYYk9ibTlyWVJJRzltT2pGeXJQcU1wWjkwODBBSGh6SWdyWXBtQ3M1RDNTbnNMcyUzRA; sara_prev_data={%22page%22:{%22article_id%22:%223ce2cb38-beda-4b96-8012-b68486d83b6d%22%2C%22channel%22:%22Panorama%22}%2C%22performance%22:{%22server_response%22:39%2C%22response_complete%22:107%2C%22page_render%22:3114%2C%22dom_complete%22:3181%2C%22total_load%22:3183%2C%22load_libraries%22:553%2C%22track_pageview%22:629}%2C%22engagement%22:{%22time_first_visible%22:69050%2C%22time_visible%22:16132%2C%22time_hidden%22:63690%2C%22time_active%22:16132%2C%22time_total%22:79822}%2C%22advertising%22:{%22free_adslots_count%22:0}}; sara_usage=4%3B1.f%3A7.f%7C1.f%3A3.f; kndctr_79655FCF5C1D42160A495E15_AdobeOrg_identity=CiY1MDM5ODA2NDUxMTYzNjEzMjg4MDUwODgwOTM3Mzk2MTYxMzc2NFITCL%2DembSzMhABGAEqBElSTDEwAKABmKvgq78yqAHatK%2Dl1OnAmQ6wAQDwAc%5FDnMK%5FMg%3D%3D; ioam2018=00136855c7f4e832f6738f762%3A1761508194446%3A1731786594446%3A.spiegel.de%3A21%3Aspiegel%3A__01_dbrsowftak_panorama%2Fgesellschaft.pf%3Anoevent%3A1735037231710%3Aj6geb6; cto_bundle=qmT-M19OclViQ0d5eHYlMkYwdHJpeEU5WDk0WW4wNnRFUk5RSmhaeCUyRmVYU0Y3clI1YjhvVVlCeFB4MUZ5TUJiREhnWkRsa2NDMXdIQUZmdHlaU0VLQ2VMbEhqZ3RuU3JRZ3hoNDZvSGdpZWU0dVJzZnBBYm9lbEtadU0lMkYxNUElMkJQOGVWNEFINEM0ck1YVkJYSGJUVUhSdVRLRWdGV01pRTdXdkloR0VnWjZocmtEQkNlbmtpRk8wMWJsNk4lMkZ2RVg1eEZBN0RXS2Q2T0JWc0pyJTJCMllNRjA0c0kyUHdRJTNEJTNE; cto_bundle=QEZbO19OclViQ0d5eHYlMkYwdHJpeEU5WDk0WW45RllkeDFNaUN5c3hRcEpDVDYlMkZZb3d3T0VIQmklMkJKQWFGMjcyQUQ2JTJGQTJqbmMxcUdwVkhzY1VDT0FGVmsxN01KZTVBY3ZvRUtVRU9qbWlHVVpwVFJaTEJUVnVWZjNWN0d3b1dEYWVaJTJGdHd5ZHVFSmV4VTZ2N0pFbllYUE5vWEJGNCUyQkExRURtd21kODRNNlFwSDMyVGttdGxWSzJFRTBCb0dJb09EcWUwMER0QXlhdGVLRWpORHpNQ1hWUXVVOEV3JTNEJTNE; cto_bundle=QEZbO19OclViQ0d5eHYlMkYwdHJpeEU5WDk0WW45RllkeDFNaUN5c3hRcEpDVDYlMkZZb3d3T0VIQmklMkJKQWFGMjcyQUQ2JTJGQTJqbmMxcUdwVkhzY1VDT0FGVmsxN01KZTVBY3ZvRUtVRU9qbWlHVVpwVFJaTEJUVnVWZjNWN0d3b1dEYWVaJTJGdHd5ZHVFSmV4VTZ2N0pFbllYUE5vWEJGNCUyQkExRURtd21kODRNNlFwSDMyVGttdGxWSzJFRTBCb0dJb09EcWUwMER0QXlhdGVLRWpORHpNQ1hWUXVVOEV3JTNEJTNE """



def translate_block(text: str) -> str:
    return LLM().call(
        prompt=f"You are an expert translator form german to english. Translate the following paragraph to English, make sure to keep the exact same structure not not add any comment only the translation: {{text}}",
        prompt_input=text,
    )


def extract_article_content(url: str) -> str:
    original_text, title = WebsiteContentExtractor().get_website_content(url, SiteSpecificConfig.DER_SPIEGEL_COOKIE_STRING)
    # cleanup
    original_text = f"""{title}
{original_text}
"""
    original_text = cleanup_content(original_text)
    return original_text

def translate_article(original_text: str) -> Generator[str, None, None]:

        #iterate over paragraphs and translate
        for paragraph in original_text.split("\n"):
            text_block = ""
            # if paragraph has less than 4 words, do not translate
            if len(paragraph.split()) < 4:
                text_block += f"{paragraph}\n"
                yield text_block
                continue

            translated_paragraph = translate_block(paragraph)

            paragraph_sentences = re.split(r'(?<=[.!?])', paragraph)
            translated_sentences = re.split(r'(?<=[.!?])', translated_paragraph)

            for index, sentence in enumerate(paragraph_sentences):
                text_block += f"{sentence}"
                if index < len(translated_sentences):
                    text_block += f" {translated_sentences[index]}"

            yield text_block
        # merge text
