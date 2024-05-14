function initiateCheckout() {
    CollectCheckout.redirectToCheckout({
      lineItems: [
        {
          sku: "{{ data.sku }}",
          quantity: "{{ data.qty }}",
          amount: "{{data.amount}}",
        },
      ],
      type: "sale",
      collectShippingInfo: true,
      customerVault: {
        addCustomer: true,
      },
      receipt: {
        showReceipt: true,
        redirectToSuccessUrl: false,
      },
    }).then((error) => {
      console.log(error);
    });
}