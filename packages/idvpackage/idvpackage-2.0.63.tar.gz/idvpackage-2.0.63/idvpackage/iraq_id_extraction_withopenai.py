import json
import time
import openai
from langchain.tools import tool
from langchain_core.runnables import RunnableLambda
from langchain.tools.render import format_tool_to_openai_function
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from pydantic import BaseModel, Field
from langchain.utils.openai_functions import convert_pydantic_to_openai_function
from typing import Optional, Literal
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser

class Verify_IRQ_ID(BaseModel):
    """Validates whether a given OCR text represents a valid Iraqi National ID (either front or back side)."""
    is_valid_id: Literal["True", "False"] = Field(..., description="Return True if document is either a valid Iraqi National ID's front side or back side." 
            "It should contain Arabic/Kurdish text like: جمهورية العراق / وزارة الداخلية"
            "مديرية الأحوال المدنية والجوازات والاقامة"
            "کوماری عیراق / وه زاره تی ناوخو"
            "پریود به را بائی باری شارستانی و پاسپورت و نیشنگه"
            "جمهورية العراق / وزارة الداخلية"
            "کوماری عیراق / وه زاره تی ناوخو"
            "Return False otherwise.")
    side: Literal["front","back",""] = Field(..., description="Determine from the given ocr text, if this is a front side or back side of an Iraqi National ID. Return empty string if its neither."
                                             "A back side has three lines of MRZ, has dates of birth, issue and expiry"
                                             "A front side has names, and id number. No dates.")

class Iraq_National_ID_front(BaseModel):
    """Extract the fields from the OCR extracted text of an Iraqi National ID's front side. Front Side has names, (like father name, mother name etc.), national id numbers but has no dates. Translate wherever required."""
    first_name: str = Field(..., description="First name (الاسم / ناو) in Arabic.")
    first_name_en: str = Field(..., description="First name (الاسم / ناو), translated to English.")
    father_name: str = Field(..., description="Father's name (الأب / باوك) in Arabic.")
    father_name_en: str = Field(..., description="Father's name (الأب / باوك), translated to English.")
    third_name: str = Field(..., description="Paternal grandfather's name (الجد / بابير) in Arabic.")
    third_name_en: str = Field(..., description="Paternal grandfather's name (الجد / بابير), translated to English.")
    last_name: Optional[str] = Field(
        "",
        description=(
            "Family/tribal name (اللقب / نازناو) in Arabic. "
            "OCR extracts various versions of 'نازناو' like الزناو, الزنار; do not interpret them as the family name."
        )
    )
    last_name_en: Optional[str] = Field(
        "",
        description=(
            "Family/tribal name (اللقب / نازناو), translated to English. "
            "OCR extracts various versions of 'نازناو' like الزناو, الزنار; do not interpret them as the family name."
        )
    )
    mother_first_name: str = Field(..., description="Mother's name (الام/ دابك) in Arabic.")
    mother_first_name_en: str = Field(..., description="Mother's name (الام/ دابك), translated to English.")
    mother_last_name: str = Field(..., description="Maternal grandfather's name (الجد / بابير) in Arabic.")
    mother_last_name_en: str = Field(..., description="Maternal grandfather's name (الجد / بابير), translated to English.")
    gender_ar: str = Field(..., description="Gender (الجنس / ردگار): ذكر (male) or أنثى (female).")
    gender: str = Field(..., description="Gender (الجنس / ردگار), translated to English")
    id_number_front: str = Field(..., description="12-digit national ID number.")
    card_number_front: Optional[str] = Field("", description="9-character alphanumeric document number.")
    serial_number: Optional[str] = Field("", description="6-digit card serial number.")
    blood_type: Optional[str] = Field(None, description="Blood type (e.g., O+, A-).")

@tool(args_schema=Iraq_National_ID_front)
def sanity_check_irq_front(
    first_name='',
    first_name_en='',
    father_name='',
    father_name_en='',
    third_name='',
    third_name_en='',
    last_name='',
    last_name_en='',
    mother_first_name='',
    mother_first_name_en='',
    mother_last_name='',
    mother_last_name_en='',
    gender_ar='',
    gender='',
    id_number_front='',
    card_number_front='',
    blood_type='',
    serial_number=''

) -> dict:
    print("SANITY CHECK IRQ FRONT WAS CALLED")
    """Run sanity checks on the data extracted from Iraq national ID's front side."""
    #Post-Processing steps
    try:
        doc_type = 'national_identity_card'
        #at this point, verify_irq_id has run, so we can safely assume the nationality here is IRQ
        nationality='IRQ'
        nationality_en = 'IRQ'

        optional_fields = ('last_name', 'last_name_en','serial_number','blood_type')
        required_fields = {k: v for k, v in locals().items() if k not in optional_fields}

        result_dict = {**locals()}

        if not last_name or not last_name_en:
            name = result_dict.get('first_name', '') + " " + result_dict.get('father_name', '')
            name_en = result_dict.get('first_name_en', '') + " " + result_dict.get('father_name_en', '')
        else:
            name = result_dict.get('first_name', '') + " " + result_dict.get('father_name', '') + result_dict.get('last_name','')
            name_en = result_dict.get('first_name_en', '') + " " + result_dict.get('father_name_en', '') + result_dict.get("last_name_en",'')

        missing = [key for key, value in required_fields.items() if not str(value).strip()]
        if missing:
            return {'error': 'covered_photo', 'error_details': f'Missing or empty fields: {", ".join(missing)}'}

        if not id_number_front.isdigit() or len(id_number_front) != 12:
            return {'error': 'covered_photo', 'error_details': 'id_number_front must be exactly 12 digits and without letters.'}


        result =  {
            "error": "",
            "error_details": "",
            **locals()
        }

        if 'required_fields' in result.keys():
            del result['required_fields']
        if 'missing' in result.keys():
            del result['missing']
        if 'optional_fields' in result.keys():
            del result['optional_fields']
        if 'result_dict' in result.keys():
            del result['result_dict']
        return result

    except Exception as e:
        return {'error':'covered_photo','error_details':e}



class Iraq_National_ID_back(BaseModel):
    """Extract only the Arabic fields from the OCR text of an Iraqi National ID's back side. A back side has fields like dates: issue, expiry, birth. Translate where required."""
    issuing_authority: str = Field(..., description="Issuing authority (جهة الاصدار / لايانى ددرجوون) in Arabic")
    issuing_authority_en: str = Field(..., description="Issuing authority (جهة الاصدار / لايانى ددرجوون), translated to English")
    issue_date: str = Field(..., description="Date of issue")
    expiry_date: str = Field(..., description="Date of expiry")
    place_of_birth: str = Field(..., description="Place of birth in Arabic.")
    place_of_birth_en: str = Field(..., description="Place of birth, translated to English.")
    dob: str = Field(..., description="Date of birth")
    family_number: str = Field(..., description='(الرقم العائلي / ژمارەى خێزانی)Family number or household number')
    mrz: str = Field(..., description="The full three line mrz, seperated often by a line seperator")
    mrz1: str = Field(..., description='MRZ Line 1')
    mrz2: str = Field(..., description="MRZ Line 2")
    mrz3: str = Field(..., description="MRZ Line 3")
    last_name_back: str = Field(...,description="Surname extracted from MRZ line 3, before the '<<' separator.")
    first_name_back: str = Field(...,description="Given name extracted from MRZ line 3, after the '<<' seperator.")


@tool(args_schema=Iraq_National_ID_back)
def sanity_check_irq_back(
    issuing_authority='',
    issuing_authority_en='',
    issue_date='',
    expiry_date='',
    place_of_birth='',
    place_of_birth_en='',
    dob='', mrz='', mrz1='', mrz2='', mrz3='',
    last_name_back='',
    first_name_back='',
    family_number=''
):
    try:
        print("SANITY CHECK IRQ BACK WAS CALLED")
        """Run sanity checks on the data extracted from Iraq national ID's back side."""
        doc_type = 'national_identity_card'
        family_number_en = family_number

        #At this point, verify_irq_id has been run, so we can safely say its an Iraqi ID.
        nationality='IRQ'
        issuing_country='IRQ'

        if mrz:
            mrz_clean = mrz.strip()
            card_number = mrz_clean[5:15]
            id_number = mrz_clean[15:27]

        else:
            return {'error':'covered_photo', 'error_details':'cropped_mrz'}

        #Check required fields
        optional_fields = ('last_name_back','first_name_back')
        required_fields = {k: v for k, v in locals().items() if k not in optional_fields}

        missing = [key for key, value in required_fields.items() if not str(value).strip()]
        if missing:
            return {
                'error': 'covered_photo',
                'error_details': f'Missing or empty fields: {", ".join(missing)}'
            }

        result =  {
            "error": "",
            "error_details": "",
            **locals()
        }

        if 'required_fields' in result.keys():
            del result['required_fields']
        if 'missing' in result.keys():
            del result['missing']
        if 'optional_fields' in result.keys():
            del result['optional_fields']
        return result
    except Exception as e:
        return {'error':'covered_photo','error_details':e}



import logging
from langchain.schema.agent import AgentFinish
def route(result, retries=3):
    if isinstance(result, AgentFinish):
        return result.return_values['output']
    else:
        tools = {
            "sanity_check_irq_back": sanity_check_irq_back,
            "sanity_check_irq_front": sanity_check_irq_front,
        }
        return tools[result.tool].run(result.tool_input)


def extraction_chain(ocr_text, openai_key, side = ''):
    gpt_model = 'gpt-4o'
    print("WE ARE IN EXTRACTION CHAIN")
    tools_func = [sanity_check_irq_back, sanity_check_irq_front]

    model = ChatOpenAI(model=gpt_model, temperature=0,
                       openai_api_key=openai_key)
    extraction_functions = [format_tool_to_openai_function(f) for f in tools_func]
    extraction_model = model.bind(functions=extraction_functions)

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "Extract the relevant information, if not explicitly provided do not guess, leave empty string. Extract partial info. Translate values wherever it is required."
         ),
        ("user", "{ocr_text}")
    ])

    prompt_verify_doc = ChatPromptTemplate.from_messages([
        ("system", "Verify the relevant documents."
         ),
        ("user", "{ocr_text}")
    ])

    model_verification = ChatOpenAI(model=gpt_model, temperature=0,
                       openai_api_key=openai_key)
    verification_function = [convert_pydantic_to_openai_function(Verify_IRQ_ID)]
    verification_model = model_verification.bind(functions=verification_function)
    verification_chain = prompt_verify_doc | verification_model | JsonOutputFunctionsParser()

    verification_model_result = verification_chain.invoke({"ocr_text":ocr_text})
    is_valid_id = verification_model_result.get("is_valid_id","False")
    side_predicted = verification_model_result.get("side")
    print("Side Predicted:", side_predicted)

    if is_valid_id=="True":
        max_retries = 3
        for attempt in range(max_retries+1):
            extraction_chain = prompt | extraction_model | OpenAIFunctionsAgentOutputParser() | route
            data = extraction_chain.invoke({"ocr_text": ocr_text})

            if data.get('error')=='':
                return data, side_predicted
            if data.get('error')!='' and attempt>=max_retries:

                return data, side_predicted
            elif data.get('error')!='' and attempt<max_retries:
                print("RETRYING")
                continue

    elif is_valid_id == "False":
        if side=='' or side=='auto':
            side = side_predicted
        if side=='front':
            return {'error':'not_front_id'}
        if side=='back':
            return {'error':'not_back_id'}
        else:
            return {'error':'covered_photo'}

