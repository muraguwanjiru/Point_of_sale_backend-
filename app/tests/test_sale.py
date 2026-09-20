import pytest
from decimal import Decimal
from fastapi import HTTPException, status
from unittest.mock import MagicMock
from  app.services.sale_service import SaleService
from  app.schemas.sale_schema import SaleCreate, SaleUpdate


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def service():
    service_instance = SaleService()
    service_instance.repository = MagicMock()
    return service_instance


def test_get_sale_success(service, mock_db):
    mock_sale = {"id": 1.0, "total_amount": "100.00"}
    service.repository.get.return_value = mock_sale

    result = service.get_sale(mock_db, 1.0)

    assert result == mock_sale
    service.repository.get.assert_called_once_with(mock_db, 1.0)


def test_get_sale_not_found(service, mock_db):
    service.repository.get.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        service.get_sale(mock_db, 999.0)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "Sale with ID 999.0 not found"


def test_get_all_sales(service, mock_db):
    mock_sales = [{"id": 1.0}, {"id": 2.0}]
    service.repository.get_all.return_value = mock_sales

    result = service.get_all_sales(mock_db)

    assert result == mock_sales
    service.repository.get_all.assert_called_once_with(mock_db)


def test_create_sale_success(service, mock_db):
    payload = MagicMock(spec=SaleCreate)
    payload.model_dump.return_value = {"total_amount": "150.50", "customer_id": 1}
    mock_created_sale = {"id": 1.0, "total_amount": Decimal("150.50")}
    service.repository.create.return_value = mock_created_sale

    result = service.create_sale(mock_db, payload)

    assert result == mock_created_sale
    service.repository.create.assert_called_once_with(mock_db, {"total_amount": "150.50", "customer_id": 1})


def test_create_sale_zero_or_negative_amount(service, mock_db):
    payload = MagicMock(spec=SaleCreate)
    payload.model_dump.return_value = {"total_amount": "0.00"}

    with pytest.raises(HTTPException) as exc_info:
        service.create_sale(mock_db, payload)

    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc_info.value.detail == "Sale total amount must be greater than zero"


def test_create_sale_invalid_format(service, mock_db):
    payload = MagicMock(spec=SaleCreate)
    payload.model_dump.return_value = {"total_amount": "invalid_number"}

    with pytest.raises(HTTPException) as exc_info:
        service.create_sale(mock_db, payload)

    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc_info.value.detail == "Invalid numerical format for total amount"


def test_update_sale_success(service, mock_db):
    mock_sale = {"id": 1.0, "total_amount": "100.00"}
    service.repository.get.return_value = mock_sale
    
    payload = MagicMock(spec=SaleUpdate)
    payload.model_dump.return_value = {"total_amount": "200.00"}
    
    mock_updated_sale = {"id": 1.0, "total_amount": Decimal("200.00")}
    service.repository.update.return_value = mock_updated_sale

    result = service.update_sale(mock_db, 1.0, payload)

    assert result == mock_updated_sale
    service.repository.update.assert_called_once_with(mock_db, mock_sale, {"total_amount": "200.00"})


def test_update_sale_invalid_amount(service, mock_db):
    mock_sale = {"id": 1.0, "total_amount": "100.00"}
    service.repository.get.return_value = mock_sale
    
    payload = MagicMock(spec=SaleUpdate)
    payload.model_dump.return_value = {"total_amount": "-50.00"}

    with pytest.raises(HTTPException) as exc_info:
        service.update_sale(mock_db, 1.0, payload)

    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc_info.value.detail == "Updated total amount must be greater than zero"


def test_delete_sale_success(service, mock_db):
    mock_sale = {"id": 1.0}
    service.repository.get.return_value = mock_sale

    result = service.delete_sale(mock_db, 1.0)

    assert result == {"detail": "Sale successfully deleted"}
    service.repository.delete.assert_called_once_with(mock_db, mock_sale)
