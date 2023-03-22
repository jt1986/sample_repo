
import pandas as pd
import pytest
from src.transformation import Transformation

@pytest.fixture
def id_values():
    id_input = pd.DataFrame({
        'id':["121asd1-123123", "78e1b0cf-fd89-4513-a648-55caa09778d5"],
        'id_split':[['121asd1','123123'], ['78e1b0cf', 'fd89', '4513', 'a648', '55caa09778d5']]
    })
    
    return id_input

@pytest.fixture
def size_values():
    size_input = pd.DataFrame({'size':[100,400,700,50,40,5]})
    return size_input


def test_transform_size(size_values):
    value = "size"
    magnitude = []
    size_expected = ["big","big", "massive", "medium", "small", "tiny"]
    obj = Transformation(None,None,None,None)
    obj.transform_size(value, size_values, magnitude)
    assert size_expected == magnitude



def test_split_id(id_values):
    value = "id_split"
    unique_id = []
    id_expected = ["121asd1", "4513"]
    obj = Transformation(None, None, None, None)
    result = obj.split_id(value, id_values, unique_id)
    assert id_expected == unique_id
