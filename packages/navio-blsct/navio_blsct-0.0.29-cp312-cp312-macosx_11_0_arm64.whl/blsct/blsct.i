%module blsct

%{
#include "../../navio-core/src/blsct/external_api/blsct.h"
%}

%constant size_t DOUBLE_PUBLIC_KEY_SIZE = DOUBLE_PUBLIC_KEY_SIZE;
%constant size_t KEY_ID_SIZE = KEY_ID_SIZE;
%constant size_t POINT_SIZE = POINT_SIZE;
%constant size_t PUBLIC_KEY_SIZE = PUBLIC_KEY_SIZE;
%constant size_t SCRIPT_SIZE = SCRIPT_SIZE;
%constant size_t SIGNATURE_SIZE = SIGNATURE_SIZE;
%constant size_t SUB_ADDR_ID_SIZE = SUB_ADDR_ID_SIZE;
%constant size_t TX_ID_SIZE = TX_ID_SIZE;
%constant size_t BLSCT_IN_AMOUNT_ERROR = BLSCT_IN_AMOUNT_ERROR;
%constant size_t BLSCT_OUT_AMOUNT_ERROR = BLSCT_OUT_AMOUNT_ERROR;

%inline %{
#define HANDLE_MEM_ALLOC_FAILURE(name) \
if (name == nullptr) { \
  printf("ERROR: Memory allocation failed\n"); \
  return nullptr; \
}

#define RETURN_RET_VAL_IF_NULL(p, ret_val) \
if (p == nullptr) { \
  printf("ERROR: " #p " is null\n"); \
  return ret_val; \
}

#define RETURN_IF_NULL(p) \
if (p == nullptr) { \
  printf("ERROR: " #p " is null\n"); \
  return; \
}

  BlsctDoublePubKey* cast_to_dpk(void* x) {
    return static_cast<BlsctDoublePubKey*>(x);
  }

  BlsctKeyId* cast_to_key_id(void* x) {
    return static_cast<BlsctKeyId*>(x);
  }

  BlsctOutPoint* cast_to_out_point(void* x) {
    return static_cast<BlsctOutPoint*>(x);
  }

  BlsctPoint* cast_to_point(void* x) {
    return static_cast<BlsctPoint*>(x);
  }

  BlsctPubKey* cast_to_pub_key(void* x) {
    return static_cast<BlsctPubKey*>(x);
  }

  BlsctRangeProof* cast_to_range_proof(void* x) {
    return static_cast<BlsctRangeProof*>(x);
  }

  BlsctScalar* cast_to_scalar(void* x) {
    return static_cast<BlsctScalar*>(x);
  }

  BlsctSignature* cast_to_signature(void* x) {
    return static_cast<BlsctSignature*>(x);
  }

  BlsctSubAddr* cast_to_sub_addr(void* x) {
    return static_cast<BlsctSubAddr*>(x);
  }

  BlsctSubAddrId* cast_to_sub_addr_id(void* x) {
    return static_cast<BlsctSubAddrId*>(x);
  }

  BlsctTokenId* cast_to_token_id(void* x) {
    return static_cast<BlsctTokenId*>(x);
  }

  CMutableTransaction* cast_to_tx(void* x) {
    return static_cast<CMutableTransaction*>(x);
  }

  CTxIn* cast_to_tx_in(void* x) {
    return static_cast<CTxIn*>(x);
  }

  CTxOut* cast_to_tx_out(void* x) {
    return static_cast<CTxOut*>(x);
  }

  uint8_t* cast_to_uint8_t_ptr(void* x) {
    return static_cast<uint8_t*>(x);
  }

  CScript* cast_to_cscript(void* x) {
    return static_cast<CScript*>(x);
  }

  BlsctAmountRecoveryReq* cast_to_amount_recovery_req(void* x) {
    return static_cast<BlsctAmountRecoveryReq*>(x);
  }

  size_t cast_to_size_t(int x) {
    return static_cast<size_t>(x);
  }

  // freeing the returned value results in error
  // swig seems to be taking care of freeing the allocated memory
  const char* to_hex(uint8_t* buf, size_t buf_size) {
    size_t dest_buf_size = 2 * buf_size + 1;

    char* s = static_cast<char*>(malloc(dest_buf_size));
    char* p = s;
    size_t n = dest_buf_size;

    for (size_t i = 0; i<buf_size; ++i) {
        snprintf(p, n, "%02x", buf[i]);
        p += 2;
        n -= 2;
    }
    return s;
  } 

  const char* as_string(void* str_buf) {
    return static_cast<const char*>(str_buf);
  }

  // uint64_vec
  void* create_uint64_vec() {
    auto vec = new(std::nothrow) std::vector<uint64_t>;
    HANDLE_MEM_ALLOC_FAILURE(vec);
    return static_cast<void*>(vec);
  }

  void free_uint64_vec(void* vp_vec) {
    if (vp_vec == nullptr) return;
    auto vec = static_cast<const std::vector<uint64_t>*>(vp_vec);
    delete vec;
  }

  void add_to_uint64_vec(
    void* vp_uint64_vec,
    const uint64_t n
  ) {
    RETURN_IF_NULL(vp_uint64_vec);
    auto uint64_vec = static_cast<std::vector<uint64_t>*>(vp_uint64_vec);

    uint64_vec->push_back(n);
  }

  // range_proof_vec
  void* create_range_proof_vec() {
    auto vec = new(std::nothrow) std::vector<bulletproofs_plus::RangeProof<Mcl>>;
    HANDLE_MEM_ALLOC_FAILURE(vec);
    return static_cast<void*>(vec);
  }

  void add_range_proof_to_vec(
    void* vp_range_proofs,
    size_t range_proof_size,
    void* vp_blsct_range_proof
  ) {
    RETURN_IF_NULL(vp_range_proofs);
    RETURN_IF_NULL(vp_blsct_range_proof);

    auto range_proofs = static_cast<std::vector<bulletproofs_plus::RangeProof<Mcl>>*>(vp_range_proofs);
    auto blsct_range_proof = static_cast<BlsctRangeProof*>(vp_blsct_range_proof);

    // unserialize range proof
    bulletproofs_plus::RangeProof<Mcl> range_proof;

    DataStream st{};
    for(size_t i=0; i<range_proof_size; ++i) {
      st << blsct_range_proof[i];
    }
    range_proof.Unserialize(st);

    // and move to the vector
    range_proofs->push_back(std::move(range_proof));
  }

  void free_range_proof_vec(const void* vp_range_proofs) {
    if (vp_range_proofs == nullptr) return;
    auto range_proofs = static_cast<const std::vector<bulletproofs_plus::RangeProof<Mcl>>*>(vp_range_proofs);
    delete range_proofs; 
  }

  // tx_in_vec
  void* create_tx_in_vec() {
    auto vec = new(std::nothrow) std::vector<BlsctTxIn>;
    HANDLE_MEM_ALLOC_FAILURE(vec);
    return static_cast<void*>(vec);
  }

  void add_tx_in_to_vec(
    void* vp_tx_ins,
    void* vp_tx_in
  ) {
    RETURN_IF_NULL(vp_tx_ins);
    RETURN_IF_NULL(vp_tx_in);

    auto tx_ins = static_cast<std::vector<BlsctTxIn>*>(vp_tx_ins);
    auto tx_in = static_cast<BlsctTxIn*>(vp_tx_in);

    tx_ins->push_back(*tx_in);
  }

  void free_tx_in_vec(const void* vp_tx_ins) {
    auto tx_ins = static_cast<const std::vector<BlsctTxIn>*>(vp_tx_ins);
    delete tx_ins; 
  }

  // tx_out_vec
  void* create_tx_out_vec() {
    auto vec = new(std::nothrow) std::vector<BlsctTxOut>;
    HANDLE_MEM_ALLOC_FAILURE(vec);
    return static_cast<void*>(vec);
  }

  void add_tx_out_to_vec(
    void* vp_tx_outs,
    void* vp_tx_out
  ) {
    RETURN_IF_NULL(vp_tx_outs);
    RETURN_IF_NULL(vp_tx_out);

    auto tx_outs = static_cast<std::vector<BlsctTxOut>*>(vp_tx_outs);
    auto tx_out = static_cast<BlsctTxOut*>(vp_tx_out);

    tx_outs->push_back(*tx_out);
  }

  void free_tx_out_vec(const void* vp_tx_outs) {
    auto tx_outs = static_cast<const std::vector<BlsctTxOut>*>(vp_tx_outs);
    delete tx_outs; 
  }

  // amount_recovery_req_vec
  void* create_amount_recovery_req_vec() {
    auto vec = new(std::nothrow) std::vector<BlsctAmountRecoveryReq>;
    RETURN_RET_VAL_IF_NULL(vec, nullptr);
    return static_cast<void*>(vec);
  }

  void add_to_amount_recovery_req_vec(
    void* vp_amt_recovery_req_vec,
    void* vp_amt_recovery_req
  ) {
    RETURN_IF_NULL(vp_amt_recovery_req_vec);
    RETURN_IF_NULL(vp_amt_recovery_req);

    auto vec = static_cast<std::vector<BlsctAmountRecoveryReq>*>(vp_amt_recovery_req_vec);
    auto req = static_cast<BlsctAmountRecoveryReq*>(vp_amt_recovery_req);
    vec->push_back(*req);
  }

  void free_amount_recovery_req_vec(void* vp_amt_recovery_req_vec) {
    RETURN_IF_NULL(vp_amt_recovery_req_vec);
    auto vec = static_cast<const std::vector<BlsctAmountRecoveryReq>*>(vp_amt_recovery_req_vec);
    delete vec;
  }

  // functions to retrieve attrs of amount recovery result 
  size_t get_amount_recovery_result_size(
    void* vp_amt_recovery_req_vec
  ) {
    if (vp_amt_recovery_req_vec == nullptr) {
    }
    auto vec = static_cast<std::vector<BlsctAmountRecoveryResult>*>(vp_amt_recovery_req_vec);
    
    return vec->size();
  }

  bool get_amount_recovery_result_is_succ(
    void* vp_amt_recovery_req_vec,
    size_t idx
  ) {
    RETURN_RET_VAL_IF_NULL(vp_amt_recovery_req_vec, 0);

    auto vec = static_cast<std::vector<BlsctAmountRecoveryResult>*>(vp_amt_recovery_req_vec);
    
    return vec->at(idx).is_succ;
  }

  uint64_t get_amount_recovery_result_amount(
    void* vp_amt_recovery_req_vec,
    size_t idx
  ) {
    RETURN_RET_VAL_IF_NULL(vp_amt_recovery_req_vec, 0);

    auto vec = static_cast<std::vector<BlsctAmountRecoveryResult>*>(vp_amt_recovery_req_vec);
    
    return vec->at(idx).amount;
  }

  const char* get_amount_recovery_result_msg(
    void* vp_amt_recovery_req_vec,
    size_t idx
  ) {
    RETURN_RET_VAL_IF_NULL(vp_amt_recovery_req_vec, nullptr);

    auto vec = static_cast<std::vector<BlsctAmountRecoveryResult>*>(vp_amt_recovery_req_vec);
    
    return vec->at(idx).msg;
  }

  uint8_t* hex_to_malloced_buf(const char* hex) {
    size_t hex_len = std::strlen(hex);
    size_t buf_len = hex_len / 2;

    uint8_t* buf = static_cast<uint8_t*>(malloc(buf_len));
    const char* p = hex;

    for (size_t i=0; i<buf_len; ++i) {
      sscanf(p, "%2hhx", &buf[i]);
      p += 2;
    }
    return buf;
  }

%}

%include "stdint.i"

#define BLSCT_RESULT uint8_t

extern enum Chain {
  MainNet,
  TestNet
};

export enum AddressEncoding {
    Bech32,
    Bech32M
};

export enum TxOutputType {
    Normal,
    StakedCommitment
};

typedef struct {
  BLSCT_RESULT result;
  void* value;
  size_t value_size;
} BlsctRetVal;

typedef struct {
  BLSCT_RESULT result;
  bool value;
} BlsctBoolRetVal;

typedef struct {
  BLSCT_RESULT result;
  void* value;
} BlsctAmountsRetVal;

typedef struct {
  BLSCT_RESULT result;
  uint8_t* ser_tx;
  size_t ser_tx_size;
  size_t in_amount_err_index;
  size_t out_amount_err_index;
} BlsctTxRetVal;

export void init();
export bool set_chain(enum Chain chain);

// freeing allocated memory
export void free_obj(void* rv);
export void free_amounts_ret_val(BlsctAmountsRetVal* rv);

// scalar
export BlsctRetVal* gen_scalar(const uint64_t n);
export BlsctRetVal* gen_random_scalar();
export uint64_t scalar_to_uint64(BlsctScalar* blsct_scalar);
export const char* scalar_to_hex(const BlsctScalar* blsct_scalar);
export BlsctRetVal* hex_to_scalar(const char* hex);
export int is_scalar_equal(const BlsctScalar* a, const BlsctScalar* b);
export const char* scalar_to_str(const BlsctScalar* blsct_scalar);

// point
export BlsctRetVal* gen_base_point();
export BlsctRetVal* gen_random_point();
export const char* point_to_hex(const BlsctPoint* blsct_point);
export BlsctRetVal* hex_to_point(const char* hex);
export int is_point_equal(const BlsctPoint* a, const BlsctPoint* b);
export const char* point_to_str(const BlsctPoint* blsct_point);
export BlsctPoint* point_from_scalar(const BlsctScalar* blsct_scalar);

// public key
export BlsctRetVal* gen_random_public_key();
export BlsctPoint* get_public_key_point(const BlsctPubKey* blsct_pub_key);
export BlsctPubKey* point_to_public_key(const BlsctPoint* blsct_point);

export BlsctRetVal* gen_double_pub_key(
  const BlsctPubKey* pk1,
  const BlsctPubKey* pk2
);

// address
export BlsctRetVal* decode_address(
  const char* blsct_enc_addr
);

export BlsctRetVal* encode_address(
  const void* blsct_dpk,
  const enum AddressEncoding encoding
);

// token id
export BlsctRetVal* gen_token_id_with_subid(
  const uint64_t token,
  const uint64_t subid
);

export BlsctRetVal* gen_token_id(
  const uint64_t token
);

export BlsctRetVal* gen_default_token_id();

export uint64_t get_token_id_token(const BlsctTokenId* blsct_token_id);

export uint64_t get_token_id_subid(const BlsctTokenId* blsct_token_id);

// range proof related
export BlsctRetVal* build_range_proof(
  const void* vp_int_vec,
  const BlsctPoint* blsct_nonce,
  const char* blsct_message,
  const BlsctTokenId* blsct_token_id
);

export BlsctBoolRetVal* verify_range_proofs(
  const void* vp_range_proofs
);

export BlsctAmountRecoveryReq* gen_recover_amount_req(
    const void* vp_blsct_range_proof,
    const size_t range_proof_size,
    const void* vp_blsct_nonce
);

export BlsctAmountsRetVal* recover_amount(
    void* vp_amt_recovery_req_vec
);

// tx related
export BlsctRetVal* gen_out_point(
    const char* tx_id_c_str,
    const uint32_t n
);

export BlsctRetVal* build_tx_in(
    const uint64_t amount,
    const uint64_t gamma,
    const BlsctScalar* spendingKey,
    const BlsctTokenId* tokenId,
    const BlsctOutPoint* outPoint,
    const bool rbf
);

export BlsctRetVal* dpk_to_sub_addr(
    const void* blsct_dpk
);

export BlsctRetVal* build_tx_out(
    const BlsctSubAddr* blsct_dest,
    const uint64_t amount,
    const char* in_memo_c_str,
    const BlsctTokenId* blsct_token_id,
    const TxOutputType output_type,
    const uint64_t min_stake
);

export BlsctTxRetVal* build_tx(
    const void* void_tx_ins,
    const void* void_tx_outs
);

export const char* get_tx_id(const CMutableTransaction* tx);

export CMutableTransaction* deserialize_tx(
    const uint8_t* ser_tx,
    const size_t ser_tx_size
);

export const std::vector<CTxIn>* get_tx_ins(const CMutableTransaction* tx);

export size_t get_tx_ins_size(const std::vector<CTxIn>* tx_ins);

export const BlsctRetVal* get_tx_in(const std::vector<CTxIn>* tx_ins, const size_t i);

export const std::vector<CTxOut>* get_tx_outs(const CMutableTransaction* tx);

export size_t get_tx_outs_size(const std::vector<CTxOut>* tx_outs);

export const BlsctRetVal* get_tx_out(const std::vector<CTxOut>* tx_outs, const size_t i);

// tx in
export const BlsctTxId* get_tx_in_prev_out_hash(const CTxIn* tx_in);

export uint32_t get_tx_in_prev_out_n(const CTxIn* tx_in);

export const BlsctScript* get_tx_in_script_sig(const CTxIn* tx_in);

export uint32_t get_tx_in_sequence(const CTxIn* tx_in);

export const BlsctScript* get_tx_in_script_witness(const CTxIn* tx_in);

// tx out
export uint64_t get_tx_out_value(const CTxOut* tx_out);

export const BlsctTokenId* get_tx_out_token_id(const CTxOut* tx_out);

export const BlsctScript* get_tx_out_script_pubkey(const CTxOut* tx_out);

export const BlsctPoint* get_tx_out_spending_key(const CTxOut* tx_out);

export const BlsctPoint* get_tx_out_ephemeral_key(const CTxOut* tx_out);

export const BlsctPoint* get_tx_out_blinding_key(const CTxOut* tx_out);

export uint16_t get_tx_out_view_tag(const CTxOut* tx_out);

export const BlsctPoint* get_tx_out_range_proof_A(const CTxOut* tx_out);
export const BlsctPoint* get_tx_out_range_proof_B(const CTxOut* tx_out);
export const BlsctPoint* get_tx_out_range_proof_r_prime(const CTxOut* tx_out);
export const BlsctPoint* get_tx_out_range_proof_s_prime(const CTxOut* tx_out);
export const BlsctPoint* get_tx_out_range_proof_delta_prime(const CTxOut* tx_out);
export const BlsctPoint* get_tx_out_range_proof_alpha_hat(const CTxOut* tx_out);
export const BlsctScalar* get_tx_out_range_proof_tau_x(const CTxOut* tx_out);

export const BlsctSignature* sign_message(
    const BlsctScalar* blsct_priv_key,
    const char* blsct_msg
);

export bool verify_msg_sig(
    const BlsctPubKey* blsct_pub_key,
    const char* blsct_msg,
    const BlsctSignature* blsct_signature
);

export BlsctPubKey* scalar_to_pub_key(
    const BlsctScalar* blsct_scalar
);

/* key derivation functions */

/* from seed */
export BlsctScalar* from_seed_to_child_key(
    const BlsctScalar* blsct_seed
);

/* from child key */
export BlsctScalar* from_child_key_to_blinding_key(
    const BlsctScalar* blsct_child_key
);

export BlsctScalar* from_child_key_to_token_key(
    const BlsctScalar* blsct_child_key
);

export BlsctScalar* from_child_key_to_tx_key(
    const BlsctScalar* blsct_child_key
);

/* from tx key */
export BlsctScalar* from_tx_key_to_view_key(
    const BlsctScalar* blsct_tx_key
);

export BlsctScalar* from_tx_key_to_spending_key(
    const BlsctScalar* blsct_tx_key
);

/* from multiple keys and other info */
export BlsctScalar* calc_priv_spending_key(
    const BlsctPubKey* blsct_blinding_pub_key,
    const BlsctScalar* blsct_view_key,
    const BlsctScalar* blsct_spending_key,
    const int64_t account,
    const uint64_t address
);

/* blsct/wallet/helpers delegators */
export uint64_t calc_view_tag(
    const BlsctPubKey* blinding_pub_key,
    const BlsctScalar* view_key
);

export BlsctKeyId* calc_hash_id(
    const BlsctPubKey* blsct_blinding_pub_key,
    const BlsctPubKey* blsct_spending_pub_key,
    const BlsctScalar* blsct_view_key
);

export const char* get_key_id_hex(
  const BlsctKeyId* blsct_key_id
);

export BlsctPubKey* calc_nonce(
    const BlsctPubKey* blsct_blinding_pub_key,
    const BlsctScalar* view_key
);

export BlsctSubAddr* derive_sub_address(
    const BlsctScalar* blsct_view_key,
    const BlsctPubKey* blsct_spending_pub_key,
    const BlsctSubAddrId* blsct_sub_addr_id
);

export BlsctSubAddrId* gen_sub_addr_id(
    const int64_t account,
    const uint64_t address
);

export int64_t get_sub_addr_id_account(
    const BlsctSubAddrId* blsct_sub_addr_id
);

export uint64_t get_sub_addr_id_address(
    const BlsctSubAddrId* blsct_sub_addr_id
);

export bool is_valid_point(
  const BlsctPoint* blsct_point
);

export BlsctDoublePubKey* gen_dpk_with_keys_and_sub_addr_id(
    const BlsctScalar* blsct_view_key,
    const BlsctPubKey* blsct_spending_pub_key,
    const int64_t account,
    const uint64_t address
);

