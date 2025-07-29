"""Transaction Builder client for ReZEN API."""

from typing import Any, BinaryIO, Dict, List, Optional, Union

from .base_client import BaseClient


class TransactionBuilderClient(BaseClient):
    """Client for transaction builder endpoints."""

    def update_title_info(
        self, transaction_id: str, title_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update title details for a transaction builder.

        Args:
            transaction_id: Transaction builder ID
            title_info: Title information data

        Returns:
            Transaction builder response data
        """
        endpoint = f"transaction-builder/{transaction_id}/title"
        return self.put(endpoint, json_data=title_info)

    def add_seller(
        self, transaction_id: str, seller_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add a new seller to a transaction builder.

        Args:
            transaction_id: Transaction builder ID
            seller_info: Seller information data

        Returns:
            Transaction builder response data
        """
        endpoint = f"transaction-builder/{transaction_id}/seller"
        return self.put(endpoint, json_data=seller_info)

    def add_referral_info(
        self,
        transaction_id: str,
        role: str,
        receives_invoice: bool,
        referral_type: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        company_name: Optional[str] = None,
        email: Optional[str] = None,
        ein: Optional[str] = None,
        phone_number: Optional[str] = None,
        address: Optional[str] = None,
        agent_id: Optional[str] = None,
        file: Optional[BinaryIO] = None,
    ) -> Dict[str, Any]:
        """Add referral info to a transaction builder.

        Note: This endpoint is marked as deprecated in the API specification.

        Args:
            transaction_id: Transaction builder ID
            role: Role type (e.g., 'REAL', 'BUYERS_AGENT', 'SELLERS_AGENT', etc.)
            receives_invoice: Whether the referral receives invoice
            referral_type: Type of referral ('EXTERNAL_ENTITY' or 'AGENT')
            first_name: First name (optional)
            last_name: Last name (optional)
            company_name: Company name (optional)
            email: Email address (optional)
            ein: EIN number (optional)
            phone_number: Phone number (optional)
            address: Address (optional)
            agent_id: Agent ID (optional)
            file: File to upload (optional)

        Returns:
            Transaction builder response data
        """
        endpoint = f"transaction-builder/{transaction_id}/referral-info"
        params = {
            "role": role,
            "receivesInvoice": receives_invoice,
            "type": referral_type,
        }

        # Add optional parameters
        if first_name:
            params["firstName"] = first_name
        if last_name:
            params["lastName"] = last_name
        if company_name:
            params["companyName"] = company_name
        if email:
            params["email"] = email
        if ein:
            params["ein"] = ein
        if phone_number:
            params["phoneNumber"] = phone_number
        if address:
            params["address"] = address
        if agent_id:
            params["agentId"] = agent_id

        files = {"file": file} if file else None
        return self._request("PUT", endpoint, params=params, files=files)

    def upload_w9_to_referral_participant(
        self, transaction_id: str, participant_id: str, file: BinaryIO
    ) -> Dict[str, Any]:
        """Upload W9 to external referral participant.

        Args:
            transaction_id: Transaction builder ID
            participant_id: Participant ID
            file: W9 file to upload

        Returns:
            Transaction builder response data
        """
        endpoint = f"transaction-builder/{transaction_id}/referral-info/{participant_id}/upload-w9"
        files = {"file": file}
        return self.put(endpoint, files=files)

    def update_price_and_date_info(
        self, transaction_id: str, price_date_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update price and date information.

        Args:
            transaction_id: Transaction builder ID
            price_date_info: Price and date information data

        Returns:
            Transaction builder response data
        """
        endpoint = f"transaction-builder/{transaction_id}/price-date-info"
        return self.put(endpoint, json_data=price_date_info)

    def update_personal_deal_info(
        self, transaction_id: str, deal_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update personal deal information.

        Args:
            transaction_id: Transaction builder ID
            deal_info: Personal deal information data

        Returns:
            Transaction builder response data
        """
        endpoint = f"transaction-builder/{transaction_id}/personal-deal-info"
        return self.put(endpoint, json_data=deal_info)

    def update_owner_info(
        self, transaction_id: str, owner_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update owner agent information.

        Args:
            transaction_id: Transaction builder ID
            owner_info: Owner agent information data

        Returns:
            Transaction builder response data
        """
        endpoint = f"transaction-builder/{transaction_id}/owner-info"
        return self.put(endpoint, json_data=owner_info)

    def add_participant(
        self, transaction_id: str, participant_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add a new participant to the transaction builder.

        Args:
            transaction_id: Transaction builder ID
            participant_info: Participant information data

        Returns:
            Transaction builder response data
        """
        endpoint = f"transaction-builder/{transaction_id}/other-participants"
        # This endpoint uses multipart/form-data according to the schema
        return self._request("PUT", endpoint, data=participant_info)

    def add_opcity(self, transaction_id: str, opcity: bool) -> Dict[str, Any]:
        """Add opcity to transaction builder.

        Args:
            transaction_id: Transaction builder ID
            opcity: Whether to enable opcity

        Returns:
            Transaction builder response data
        """
        endpoint = f"transaction-builder/{transaction_id}/opcity"
        params = {"opcity": opcity}
        return self._request("PUT", endpoint, params=params)

    def update_mortgage_info(
        self, transaction_id: str, mortgage_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update mortgage information.

        Args:
            transaction_id: Transaction builder ID
            mortgage_info: Mortgage information data

        Returns:
            Transaction builder response data
        """
        endpoint = f"transaction-builder/{transaction_id}/mortgage-info"
        return self.put(endpoint, json_data=mortgage_info)

    def update_location_info(
        self, transaction_id: str, location_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update location information.

        Args:
            transaction_id: Transaction builder ID
            location_info: Location information data

        Returns:
            Transaction builder response data
        """
        endpoint = f"transaction-builder/{transaction_id}/location-info"
        return self.put(endpoint, json_data=location_info)

    def update_fmls_info(
        self, transaction_id: str, fmls_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update whether this builder's property is listed on FMLS.

        Args:
            transaction_id: Transaction builder ID
            fmls_info: FMLS information data

        Returns:
            Transaction builder response data
        """
        endpoint = f"transaction-builder/{transaction_id}/fmls"
        return self.put(endpoint, json_data=fmls_info)

    def add_double_ender_agent(
        self, transaction_id: str, agent_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add double-ender agent to the transaction builder.

        Args:
            transaction_id: Transaction builder ID
            agent_info: Double-ender agent information data

        Returns:
            Transaction builder response data
        """
        endpoint = f"transaction-builder/{transaction_id}/double-ender-agent"
        return self.put(endpoint, json_data=agent_info)

    def add_commission_payer(
        self, transaction_id: str, commission_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add commission payer information.

        Args:
            transaction_id: Transaction builder ID
            commission_info: Commission payer information data

        Returns:
            Transaction builder response data
        """
        endpoint = f"transaction-builder/{transaction_id}/commission-payer"
        # This endpoint uses multipart/form-data according to the schema
        return self._request("PUT", endpoint, data=commission_info)

    def update_commission_splits(
        self, transaction_id: str, commission_splits: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Update commission splits information.

        Args:
            transaction_id: Transaction builder ID
            commission_splits: List of commission split data

        Returns:
            Transaction builder response data
        """
        endpoint = f"transaction-builder/{transaction_id}/commission-info"
        return self._request("PUT", endpoint, json_data=commission_splits)

    def add_co_agent(
        self, transaction_id: str, co_agent_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add a new co-agent.

        Args:
            transaction_id: Transaction builder ID
            co_agent_info: Co-agent information data

        Returns:
            Transaction builder response data
        """
        endpoint = f"transaction-builder/{transaction_id}/co-agent"
        return self.put(endpoint, json_data=co_agent_info)

    def add_buyer(
        self, transaction_id: str, buyer_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add a new buyer.

        Args:
            transaction_id: Transaction builder ID
            buyer_info: Buyer information data

        Returns:
            Transaction builder response data
        """
        endpoint = f"transaction-builder/{transaction_id}/buyer"
        return self.put(endpoint, json_data=buyer_info)

    def update_buyer_and_seller_info(
        self, transaction_id: str, buyer_seller_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update buyer and seller information.

        Args:
            transaction_id: Transaction builder ID
            buyer_seller_info: Buyer and seller information data

        Returns:
            Transaction builder response data
        """
        endpoint = f"transaction-builder/{transaction_id}/buyer-seller-info"
        return self.put(endpoint, json_data=buyer_seller_info)

    def update_additional_fees_info(
        self, transaction_id: str, fees_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update additional fees information.

        Args:
            transaction_id: Transaction builder ID
            fees_info: Additional fees information data

        Returns:
            Transaction builder response data
        """
        endpoint = f"transaction-builder/{transaction_id}/additional-fees-info"
        return self.put(endpoint, json_data=fees_info)

    def add_referral_info_v2(
        self, transaction_id: str, referral_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add referral info (v2 endpoint).

        Args:
            transaction_id: Transaction builder ID
            referral_info: Referral information data

        Returns:
            Builder participant data
        """
        endpoint = f"transaction-builder/{transaction_id}/add-referral-info"
        return self.put(endpoint, json_data=referral_info)

    # GET endpoints
    def get_transaction_builders(
        self,
        limit: int,
        from_offset: int,
        yenta_id: str,
        builder_type: str = "TRANSACTION",
    ) -> Dict[str, Any]:
        """Get a paginated list of transaction builders.

        Args:
            limit: Maximum number of results to return
            from_offset: Starting offset for pagination
            yenta_id: User ID
            builder_type: Type of builder ('TRANSACTION' or 'LISTING')

        Returns:
            Paginated list of transaction builders
        """
        endpoint = "transaction-builder"
        params = {
            "limit": limit,
            "from": from_offset,
            "yentaId": yenta_id,
            "type": builder_type,
        }
        return self.get(endpoint, params=params)

    def get_transaction_builders_paged(
        self,
        limit: int,
        from_offset: int,
        yenta_id: str,
        builder_type: str = "TRANSACTION",
    ) -> Dict[str, Any]:
        """Get a paginated list of transaction builders (alternative endpoint).

        Args:
            limit: Maximum number of results to return
            from_offset: Starting offset for pagination
            yenta_id: User ID
            builder_type: Type of builder ('TRANSACTION' or 'LISTING')

        Returns:
            Paginated list of transaction builders
        """
        endpoint = "transaction-builder/paged"
        params = {
            "limit": limit,
            "from": from_offset,
            "yentaId": yenta_id,
            "type": builder_type,
        }
        return self.get(endpoint, params=params)

    def get_transaction_builder(self, transaction_id: str) -> Dict[str, Any]:
        """Get a specific transaction builder by ID.

        Args:
            transaction_id: Transaction builder ID

        Returns:
            Transaction builder data
        """
        endpoint = f"transaction-builder/{transaction_id}"
        return self.get(endpoint)

    def get_builder_features(self, transaction_id: str) -> Dict[str, Any]:
        """Get optional features available for the transaction being built.

        Args:
            transaction_id: Transaction builder ID

        Returns:
            Available features data
        """
        endpoint = f"transaction-builder/{transaction_id}/features"
        return self.get(endpoint)

    def get_eligible_for_mortgage_ecp(self, transaction_id: str) -> Dict[str, Any]:
        """Check if transaction builder is eligible for mortgage ECP.

        Args:
            transaction_id: Transaction builder ID

        Returns:
            Eligibility status
        """
        endpoint = f"transaction-builder/{transaction_id}/eligible-for-mortgage-ecp"
        return self.get(endpoint)

    def get_commission_payer_roles_and_display_name(
        self, transaction_id: str
    ) -> Dict[str, Any]:
        """Get commission payer roles and display names for transaction builder.

        Args:
            transaction_id: Transaction builder ID

        Returns:
            Commission payer roles and display names
        """
        endpoint = f"transaction-builder/{transaction_id}/commission-payer-roles-and-display-name"
        return self.get(endpoint)

    def get_commission_payer_roles(self) -> Dict[str, Any]:
        """Get available commission payer roles.

        Returns:
            Available commission payer roles
        """
        endpoint = "transaction-builder/commission-payer-roles"
        return self.get(endpoint)

    def get_commission_payer_roles_and_display_names(self) -> Dict[str, Any]:
        """Get commission payer roles and their display names.

        Returns:
            Commission payer roles with display names
        """
        endpoint = "transaction-builder/commission-payer-roles-and-display-name"
        return self.get(endpoint)

    def get_metadata_for_participant_creation(
        self, transaction_id: str, participant_role: str
    ) -> Dict[str, Any]:
        """Get metadata required to create a participant.

        Args:
            transaction_id: Transaction builder ID
            participant_role: Role of the participant to be created

        Returns:
            Metadata for participant creation
        """
        endpoint = f"transaction-builder/{transaction_id}/metadata-for-participant-creation/{participant_role}"
        return self.get(endpoint)

    # POST endpoints
    def create_transaction_builder(self, builder_type: str = "TRANSACTION") -> str:
        """Create empty transaction builder.

        Args:
            builder_type: Type of builder ('TRANSACTION' or 'LISTING')

        Returns:
            Transaction builder ID
        """
        endpoint = "transaction-builder"
        params = {"type": builder_type}
        response = self._request("POST", endpoint, params=params)
        return str(response.get("id", ""))

    def create_builder_from_transaction(self, transaction_id: str) -> Dict[str, Any]:
        """Create transaction builder from given transaction.

        Args:
            transaction_id: Transaction ID to create builder from

        Returns:
            Transaction builder response data
        """
        endpoint = f"transaction-builder/{transaction_id}/transaction-to-builder"
        return self.post(endpoint)

    def add_transaction_coordinator(
        self, transaction_id: str, yenta_id: str
    ) -> Dict[str, Any]:
        """Add transaction coordinator to transaction builder.

        Args:
            transaction_id: Transaction builder ID
            yenta_id: Coordinator user ID

        Returns:
            Transaction builder response data
        """
        endpoint = (
            f"transaction-builder/{transaction_id}/transaction-coordinator/{yenta_id}"
        )
        return self.post(endpoint)

    def submit_transaction(self, transaction_id: str) -> Dict[str, Any]:
        """Submit a transaction builder to create a transaction.

        Args:
            transaction_id: Transaction builder ID

        Returns:
            Transaction preview response data
        """
        endpoint = f"transaction-builder/{transaction_id}/submit"
        return self.post(endpoint)

    def update_title_contract(
        self, transaction_id: str, title_contract_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update title contract information.

        Args:
            transaction_id: Transaction builder ID
            title_contract_info: Title contract information data

        Returns:
            Transaction builder response data
        """
        endpoint = f"transaction-builder/{transaction_id}/title-contract"
        return self.put(endpoint, json_data=title_contract_info)

    def mortgage_ecp_opt_out(self, transaction_id: str) -> Dict[str, Any]:
        """Opt out of mortgage ECP for transaction builder.

        Args:
            transaction_id: Transaction builder ID

        Returns:
            Transaction builder response data
        """
        endpoint = f"transaction-builder/{transaction_id}/mortgage-ecp-opt-out"
        return self.put(endpoint)

    def mortgage_ecp_opt_in(self, transaction_id: str) -> Dict[str, Any]:
        """Opt in to mortgage ECP for transaction builder.

        Args:
            transaction_id: Transaction builder ID

        Returns:
            Transaction builder response data
        """
        endpoint = f"transaction-builder/{transaction_id}/mortgage-ecp-opt-in"
        return self.put(endpoint)

    # DELETE endpoints
    def delete_transaction_builder(self, transaction_id: str) -> Dict[str, Any]:
        """Delete transaction builder.

        Args:
            transaction_id: Transaction builder ID

        Returns:
            Deletion response data
        """
        endpoint = f"transaction-builder/{transaction_id}"
        return self.delete(endpoint)

    # Individual resource endpoints
    def get_seller(self, transaction_id: str, seller_id: str) -> Dict[str, Any]:
        """Get specific seller information.

        Args:
            transaction_id: Transaction builder ID
            seller_id: Seller ID

        Returns:
            Seller data
        """
        endpoint = f"transaction-builder/{transaction_id}/seller/{seller_id}"
        return self.get(endpoint)

    def update_seller(
        self, transaction_id: str, seller_id: str, seller_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update specific seller information.

        Args:
            transaction_id: Transaction builder ID
            seller_id: Seller ID
            seller_info: Updated seller information

        Returns:
            Transaction builder response data
        """
        endpoint = f"transaction-builder/{transaction_id}/seller/{seller_id}"
        return self.put(endpoint, json_data=seller_info)

    def delete_seller(self, transaction_id: str, seller_id: str) -> Dict[str, Any]:
        """Delete specific seller.

        Args:
            transaction_id: Transaction builder ID
            seller_id: Seller ID

        Returns:
            Deletion response data
        """
        endpoint = f"transaction-builder/{transaction_id}/seller/{seller_id}"
        return self.delete(endpoint)

    def get_referral_participant(
        self, transaction_id: str, participant_id: str
    ) -> Dict[str, Any]:
        """Get specific referral participant information.

        Args:
            transaction_id: Transaction builder ID
            participant_id: Participant ID

        Returns:
            Referral participant data
        """
        endpoint = (
            f"transaction-builder/{transaction_id}/referral-info/{participant_id}"
        )
        return self.get(endpoint)

    def update_referral_participant(
        self, transaction_id: str, participant_id: str, participant_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update specific referral participant information.

        Args:
            transaction_id: Transaction builder ID
            participant_id: Participant ID
            participant_info: Updated participant information

        Returns:
            Transaction builder response data
        """
        endpoint = (
            f"transaction-builder/{transaction_id}/referral-info/{participant_id}"
        )
        return self.put(endpoint, json_data=participant_info)

    def delete_referral_participant(
        self, transaction_id: str, participant_id: str
    ) -> Dict[str, Any]:
        """Delete specific referral participant.

        Args:
            transaction_id: Transaction builder ID
            participant_id: Participant ID

        Returns:
            Deletion response data
        """
        endpoint = (
            f"transaction-builder/{transaction_id}/referral-info/{participant_id}"
        )
        return self.delete(endpoint)

    def get_other_participant(
        self, transaction_id: str, participant_id: str
    ) -> Dict[str, Any]:
        """Get specific other participant information.

        Args:
            transaction_id: Transaction builder ID
            participant_id: Participant ID

        Returns:
            Other participant data
        """
        endpoint = (
            f"transaction-builder/{transaction_id}/other-participants/{participant_id}"
        )
        return self.get(endpoint)

    def update_other_participant(
        self, transaction_id: str, participant_id: str, participant_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update specific other participant information.

        Args:
            transaction_id: Transaction builder ID
            participant_id: Participant ID
            participant_info: Updated participant information

        Returns:
            Transaction builder response data
        """
        endpoint = (
            f"transaction-builder/{transaction_id}/other-participants/{participant_id}"
        )
        return self.put(endpoint, json_data=participant_info)

    def delete_other_participant(
        self, transaction_id: str, participant_id: str
    ) -> Dict[str, Any]:
        """Delete specific other participant.

        Args:
            transaction_id: Transaction builder ID
            participant_id: Participant ID

        Returns:
            Deletion response data
        """
        endpoint = (
            f"transaction-builder/{transaction_id}/other-participants/{participant_id}"
        )
        return self.delete(endpoint)

    def get_co_agent(self, transaction_id: str, co_agent_id: str) -> Dict[str, Any]:
        """Get specific co-agent information.

        Args:
            transaction_id: Transaction builder ID
            co_agent_id: Co-agent ID

        Returns:
            Co-agent data
        """
        endpoint = f"transaction-builder/{transaction_id}/co-agent/{co_agent_id}"
        return self.get(endpoint)

    def update_co_agent(
        self, transaction_id: str, co_agent_id: str, co_agent_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update specific co-agent information.

        Args:
            transaction_id: Transaction builder ID
            co_agent_id: Co-agent ID
            co_agent_info: Updated co-agent information

        Returns:
            Transaction builder response data
        """
        endpoint = f"transaction-builder/{transaction_id}/co-agent/{co_agent_id}"
        return self.put(endpoint, json_data=co_agent_info)

    def delete_co_agent(self, transaction_id: str, co_agent_id: str) -> Dict[str, Any]:
        """Delete specific co-agent.

        Args:
            transaction_id: Transaction builder ID
            co_agent_id: Co-agent ID

        Returns:
            Deletion response data
        """
        endpoint = f"transaction-builder/{transaction_id}/co-agent/{co_agent_id}"
        return self.delete(endpoint)

    def get_buyer(self, transaction_id: str, buyer_id: str) -> Dict[str, Any]:
        """Get specific buyer information.

        Args:
            transaction_id: Transaction builder ID
            buyer_id: Buyer ID

        Returns:
            Buyer data
        """
        endpoint = f"transaction-builder/{transaction_id}/buyer/{buyer_id}"
        return self.get(endpoint)

    def update_buyer(
        self, transaction_id: str, buyer_id: str, buyer_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update specific buyer information.

        Args:
            transaction_id: Transaction builder ID
            buyer_id: Buyer ID
            buyer_info: Updated buyer information

        Returns:
            Transaction builder response data
        """
        endpoint = f"transaction-builder/{transaction_id}/buyer/{buyer_id}"
        return self.put(endpoint, json_data=buyer_info)

    def delete_buyer(self, transaction_id: str, buyer_id: str) -> Dict[str, Any]:
        """Delete specific buyer.

        Args:
            transaction_id: Transaction builder ID
            buyer_id: Buyer ID

        Returns:
            Deletion response data
        """
        endpoint = f"transaction-builder/{transaction_id}/buyer/{buyer_id}"
        return self.delete(endpoint)
